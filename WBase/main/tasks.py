from workers import task
import requests
import json
import time
#from django.shortcuts import render
from django.conf import settings
from .models import Material, Can, Batch_pr, W_user, Weighting, Lot, Declared_Batches
from requests.exceptions import ConnectionError


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

@task(schedule=300)
def upload():
    print(str(time.time())+"  -  "+"Task running!")
    try:
        w_types = settings.GLOBAL_SETTINGS["W_LIST"]
        ip = settings.GLOBAL_SETTINGS["API_SERVER_URL"]
        docs_list = []
        request_prefix = "http://"
        #request_postfix = "/MobileSMARTS/api/v1/Docs/Vzveshivanie?$count=true"
        request_postfix = "/MobileSMARTS/api/v1/Docs?$count=true"
        request_txt = request_prefix + ip + request_postfix
        response = requests.get(request_txt)
        status = response.status_code
        if status == 200:
            data = response.json()
            quant = data["@odata.count"]
            if quant != 0:
                docs_list = data
                for one_doc in docs_list["value"]:
                    if one_doc["documentTypeName"] in w_types:
                        print("Беру")
                        new_batch_obj, _ = Batch_pr.objects.get_or_create(
                            batch_name=one_doc["Varka"]
                        )
                        new_w_user_obj, _ = W_user.objects.get_or_create(
                            w_user_name=one_doc["Vypolnil"]
                        )
                        new_can_obj, can_status = Can.objects.get_or_create(
                            can_id=one_doc["ShtrihkodEmkosti"],
                            can_batch=new_batch_obj,
                            can_user=new_w_user_obj,
                        )
                        if can_status:
                            doc_rows = get_document_rows(one_doc["id"])
                            if doc_rows["@odata.count"] != 0:
                                for one_row in doc_rows["value"]:
                                    new_material_obj, _ = Material.objects.update_or_create(
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
                        else:
                            pass
                    else:
                        pass
                        print("Не беру")
            else:
                pass
                #print("No docs to works!")
        else:
            pass
            #print("Server not responce!")
    except requests.exceptions.ConnectionError:
        pass
        #print("API Server connection error!")

''' 
@task(schedule=300)
def upload_decl():
    print("Upload declared!")
    try:
        ip = settings.GLOBAL_SETTINGS["API_SERVER_URL"]
        request_prefix = "http://"
        request_postfix = "/MobileSMARTS/api/v1/Tables/Batches"
        request_txt = request_prefix + ip + request_postfix
        response = requests.get(request_txt)
        status = response.status_code
        if status == 200:
            data = response.json()
            table_rows = data
            for one_row in table_rows["value"]:
                new_batch_obj, _ = Batch_pr.objects.get_or_create(
                    batch_name=one_row["batch"],
                )
                new_material_obj, _ = Material.objects.get_or_create(
                    code=one_row["code"],
                    material_name=one_row["name"],
                )
                new_declared_datches_obj, _ = Declared_Batches.objects.get_or_create(
                    batch_pr=new_batch_obj,
                    material=new_material_obj,
                    decl_quant=one_row["quant"],
                )
            print("Declared done!")
        else:
            pass
    except requests.exceptions.ConnectionError:
        pass
 '''

