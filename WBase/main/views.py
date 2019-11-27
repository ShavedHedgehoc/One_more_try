import requests
import json
import time
from django.shortcuts import render
from django.conf import settings
from .models import Material, Can, Batch_pr, W_user, Weighting, Lot
from requests.exceptions import ConnectionError

# Create your views here.
# Запрос партий производителя
# http://srv-webts:9504/MobileSMARTS/api/v1/Tables/Lotpr
# http://localhost:9504/MobileSMARTS/api/v1/Tables/Lotpr('05554004171504201402')


def get_producer_lot():
    lot_id = "05554192102908201801"
    request_txt = (
        "http://192.168.1.13:9504/MobileSMARTS/api/v1/Tables/Lotpr('" + lot_id + "')"
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
        response = requests.get("http://srv-webts:9504/MobileSMARTS/api/v1/Products")
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
    try:
        response = requests.get(
            "http://srv-webts:9504/MobileSMARTS/api/v1/Docs/Vzveshivanie?$select=none&$count=true"
        )
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
                                new_lot_obj,_=Lot.objects.get_or_create(
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

    return render(request, "index.html", {"list": product_list})


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

