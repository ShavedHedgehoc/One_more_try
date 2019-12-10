import requests
import json
import time
from django.shortcuts import render
from django.conf import settings
from .models import Material, Can, Batch_pr, W_user, Weighting, Lot, Declared_Batches
from requests.exceptions import ConnectionError
from django.views.generic.list import ListView
from django.db.models import Sum, Count

# Create your views here.
# Запрос партий производителя
# http://srv-webts:9504/MobileSMARTS/api/v1/Tables/Lotpr
# http://localhost:9504/MobileSMARTS/api/v1/Tables/Lotpr('05554004171504201402')


def get_producer_lot():
    lot_id = "05554192102908201801"
    request_txt = (
        "http://192.168.1.13:9504/MobileSMARTS/api/v1/Tables/Lotpr('" +
        lot_id + "')"
    )
    # request_txt = (
    #     "http://srv-webts:9504/MobileSMARTS/api/v1/Tables/Lotpr('" + lot_id + "')"
    # )
    # start = time.time()
    try:
        response = requests.get(request_txt)
        data = response.status_code
    except:
        return "Ошибка!"
    return data  # time.time()-start


def get_products():
    start = time.time()
    try:
        response = requests.get(
            "http://srv-webts:9504/MobileSMARTS/api/v1/Products")
        data = response.json()
        for one_record in data["value"]:
            material, _ = Material.objects.get_or_create(
                code=one_record["id"], material_name=one_record["name"],
            )
    except:
        print(
            "Ошибка",
            one_record["name"],
            "_" + one_record["packings"][0]["barcode"] + "_",
        )

    # materials=[]
    # for one_record in data['value']:
    #     a={
    #     'id':one_record['id'],
    #     'marking':one_record['marking'],
    #     'name':one_record['name'],
    #     'unit':one_record['packings'][0]['name'],
    #     'barcode':one_record['packings'][0]['barcode'],
    #     }
    #     materials.append(a)

    return time.time() - start


def get_documents_list():
    try:
        response = requests.get(
            "http://srv-webts:9504/MobileSMARTS/api/v1/Docs/Vzveshivanie?$count=true"
        )
        data = response.json()
        quant = data["@odata.count"]
        # if quant>0:

    except:
        pass
    return get_data


def get_document_rows(doc_id):
    ip = settings.GLOBAL_SETTINGS["API_SERVER_URL"]
    try:
        # HTTP STATUS!!!
        request_prefix = "http://" + ip + "/MobileSMARTS/api/v1/Docs('"
        request_postfix = ")/declaredItems?$expand=product&$count=true"
        request_full = request_prefix + doc_id + request_postfix
        response = requests.get(request_full)
        get_data = response.json()
    except requests.exceptions.ConnectionError:
        print("API Server connection error!")
    return get_data


def get_documents_quant():
    ip = settings.GLOBAL_SETTINGS["API_SERVER_URL"]
    try:
        request_prefix = "http://"
        request_postfix = "/MobileSMARTS/api/v1/Docs/Vzveshivanie?$select=none&$count=true"
        response = requests.get(request_prefix+ip+request_postfix)
        data = response.json()
        quant = data["@odata.count"]
    except:
        quant = "Server not found"
    return quant


def delete_document(doc_id):
    request_prefix = "http://srv-webts:9504/MobileSMARTS/api/v1/Docs('"
    request_postfix = ")"
    request_full = request_prefix + doc_id + request_postfix
    requests.delete(request_full)
    return


def index(request):
    doc_quant = get_documents_quant()
    return render(request, "index.html", {"list": doc_quant})


def upload(request):
    try:
        ip = settings.GLOBAL_SETTINGS["API_SERVER_URL"]
        docs_list = []
        request_prefix = "http://"
        request_postfix = "/MobileSMARTS/api/v1/Docs/Vzveshivanie?$count=true"
        request_txt = request_prefix + ip + request_postfix
        response = requests.get(request_txt)
        status = response.status_code
        print(status)
        if status == 200:
            data = response.json()
            quant = data["@odata.count"]
            if quant != 0:
                print("Works with docs!")
                docs_list = data
                for one_doc in docs_list["value"]:
                    new_batch_obj, _ = Batch_pr.objects.get_or_create(
                        batch_name=one_doc["Varka"]
                    )
                    print(new_batch_obj)
                    new_w_user_obj, _ = W_user.objects.get_or_create(
                        w_user_name=one_doc["Vypolnil"]
                    )
                    print(new_w_user_obj)
                    new_can_obj, can_status = Can.objects.get_or_create(
                        can_id=one_doc["ShtrihkodEmkosti"],
                        can_batch=new_batch_obj,
                        can_user=new_w_user_obj,
                    )
                    print(new_can_obj)
                    if can_status:
                        doc_rows = get_document_rows(one_doc["id"])
                        if doc_rows["@odata.count"] != 0:
                            for one_row in doc_rows["value"]:
                                new_material_obj, _ = Material.objects.get_or_create(
                                    code=one_row["product"]["id"],
                                    material_name=one_row["product"]["name"],
                                )
                                print(new_material_obj)
                                new_lot_obj, _ = Lot.objects.get_or_create(
                                    lot_code=one_row["Partiya"],
                                    material=new_material_obj,
                                )
                                new_weighting_obj, _ = Weighting.objects.get_or_create(
                                    weighting_id=new_can_obj,
                                    material=new_material_obj,
                                    lot=new_lot_obj,
                                    quantity=one_row["currentQuantity"],
                                )

                        product_list = doc_rows
                    else:
                        print("Не беру строки")
                        product_list = "Хуй"
            else:
                print("No docs to works!")
                product_list = ["No docs to works!"]
        else:
            print("Server not responce!")

    except requests.exceptions.ConnectionError:
        print("API Server connection error!")

    return render(request, "index.html")


def index2(request):
    product_list = get_products()

    docs_list = get_documents_list()
    sss = []
    for one_doc in docs_list["value"]:
        # sss.append(one_doc)
        lll = get_document_rows(one_doc["id"])
        for one_row in lll["value"]:
            d = [
                one_doc["ShtrihkodEmkosti"],
                one_row["product"]["id"],
                one_row["product"]["name"],
                one_row["currentQuantity"],
            ]
            sss.append(d)
    #   if

    #    delete_document(one_doc['id'])
    #     request_prefix="http://srv-webts:9504/MobileSMARTS/api/v1/Docs('"
    #     request_postfix=")"
    #     request_full=request_prefix+one_doc['id']+request_postfix
    #     responce=requests.delete(request_full)

    return render(request, "index.html", {"list": product_list})


class Batch_view(ListView):
    template_name = "batch_view.html"

    def get_queryset(self, **kwargs):
        queryset = Batch_pr.objects.all()
        return queryset

    def get_cur_month(self, **kwargs):
        m = "C"
        return m

    def get_cur_year(self, **kwargs):
        y = 9
        return y

    def get_decl_rows_count(self, **kwargs):
        batch = self.kwargs['batch_name']
        d_count = Declared_Batches.objects.filter(
            batch_pr__batch_name=batch).count()
        return d_count

    def get_context_data(self, **kwargs):
        context = super(Batch_view, self).get_context_data(**kwargs)
        f_year = self.get_cur_year()
        f_month = self.get_cur_month()
        filter_set = self.get_queryset()

        filter_set = Batch_pr.objects.annotate(
            d=Count('declared_batches', distinct=True),
            w=Count('can__weighting__material', distinct=True)
        ).filter(b_month=f_month, b_year=f_year)

        context['records'] = filter_set
        return context


class Varka_view(ListView):
    template_name = "listvar.html"

    def get_queryset(self, **kwargs):
        queryset = Declared_Batches.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        varka = self.kwargs['batch']
        context = super(Varka_view, self).get_context_data(**kwargs)
        filter_set = self.get_queryset()
        filter_set = filter_set.filter(batch_pr__batch_name=varka)
        records = []
        for f in filter_set:
            m_rws_qount = Weighting.objects.filter(
                weighting_id__can_batch__batch_name=f.batch_pr.batch_name
            ).filter(
                material__code=f.material.code
            ).count()
            lots_list = []
            w_quant = 0
            if m_rws_qount > 0:
                m_rws = Weighting.objects.filter(
                    weighting_id__can_batch__batch_name=f.batch_pr.batch_name
                ).filter(
                    material__code=f.material.code
                )
                lots_rows = m_rws.values(
                    'lot__lot_code').annotate(Sum('quantity'))

                w_quant = m_rws.aggregate(Sum('quantity'))['quantity__sum']
                for one_lot in lots_rows:
                    lot = {
                        'lot': one_lot['lot__lot_code'],
                        'quant': one_lot['quantity__sum'],
                    }
                    lots_list.append(lot)
            row = {
                'code': f.material.code,
                'name': f.material.material_name,
                'decl_quantity': f.decl_quant,
                'cur_quantity': w_quant,
                'lots': lots_list,
            }
            records.append(row)

        # f_set= filter_set.values('prod_material__code')

        # # ff_set=Weighting.objects.filter(batch__batch_name="100D9", material__code__in=f_set).annotate(ss=Sum('quantity'))
        # # fff_set =ff_set.values('material','lot').annotate(ss=Sum('quantity'))
        # filter_set = filter_set.filter(prod_batch__batch_name="100D9")
        # context['records2'] = f_set
        # f_obj=filter_set.values('prod_material__code','prod_material__material_name').annotate(tt=Sum('prod_decl_quantity'))
        # filter_set = filter_set.values('prod_batch','prod_material').annotate(tt=Sum('prod_decl_quantity'))
        # # filter_set = filter_set.filter(prod_batch__batch_name="101D9").annotate(tt=Sum('prod_decl_quantity'))
        # ff_set=Weighting.objects.filter(batch__batch_name="100D9").values('batch')
        # context['records3'] = filter_set

        #context['records3'] = rec
        #context['records','r2'] = (filter_set,a)

        context['records'] = records
        return context
