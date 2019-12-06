from workers import task
import requests
import json
import time
import datetime

# from django.shortcuts import render
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


def get_now():
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return now


@task(schedule=30)
def upload():
    print("%s  -  Upload documents running!" % get_now())
    start = time.time()
    try:
        w_types = settings.GLOBAL_SETTINGS["W_LIST"]
        ip = settings.GLOBAL_SETTINGS["API_SERVER_URL"]
        docs_list = []
        request_prefix = "http://"
        request_postfix = "/MobileSMARTS/api/v1/Docs?$count=true"
        request_txt = request_prefix + ip + request_postfix
        response = requests.get(request_txt)
        status = response.status_code
        if status == 200:
            print("%s - 200 Request OK!" % get_now())
            data = response.json()
            quant = data["@odata.count"]
            if quant != 0:
                print("Get %s docs" % quant)
                docs_list = data
                for one_doc in docs_list["value"]:
                    if one_doc["documentTypeName"] in w_types:
                        print("Document %s processing..." % one_doc["name"])
                        (
                            new_batch_obj,
                            new_batch_status,
                        ) = Batch_pr.objects.get_or_create(batch_name=one_doc["Varka"])
                        if new_batch_status:
                            print("Created new batch %s..." % one_doc["Varka"])
                        new_w_user_obj, new_user_status = W_user.objects.get_or_create(
                            w_user_name=one_doc["Vypolnil"]
                        )
                        if new_user_status:
                            print("Created new user %s..." % one_doc["Vypolnil"])
                        new_can_obj, new_can_status = Can.objects.get_or_create(
                            can_id=one_doc["ShtrihkodEmkosti"],
                            can_batch=new_batch_obj,
                            can_user=new_w_user_obj,
                        )
                        if new_can_status:
                            print("Created new can %s..." % one_doc["ShtrihkodEmkosti"])
                            doc_rows = get_document_rows(one_doc["id"])
                            if doc_rows["@odata.count"] != 0:
                                count = 0
                                for one_row in doc_rows["value"]:
                                    try:
                                        new_material_obj = Material.objects.get(
                                            code=one_row["product"]["id"]
                                        )
                                    except Material.DoesNotExist:
                                        new_material_obj = Material(
                                            code=one_row["product"]["id"],
                                            material_name=one_row["product"]["name"],
                                        )
                                        new_material_obj.save()
                                        print(
                                            "Created new material %s %s"
                                            % (one_row["product"]["id"], one_row["product"]["name"])
                                        )
                                    except:
                                        print(
                                            "ERROR with %s %s!"
                                            % (
                                                one_row["product"]["id"],
                                                one_row["product"]["name"],
                                            )
                                        )
                                    try:
                                        (
                                            new_lot_obj,
                                            new_lot_status,
                                        ) = Lot.objects.get_or_create(
                                            lot_code=one_row["Partiya"],
                                            material=new_material_obj,
                                        )
                                        if new_lot_status:
                                            print(
                                                "Created new lot %s..."
                                                % (one_row["Partiya"])
                                            )
                                    except:
                                        print(
                                            "ERROR with lot %s..."
                                            % (one_row["Partiya"])
                                        )
                                    try:
                                        (
                                            new_weighting_obj,
                                            new_weighting_status,
                                        ) = Weighting.objects.get_or_create(
                                            weighting_id=new_can_obj,
                                            material=new_material_obj,
                                            lot=new_lot_obj,
                                            quantity=one_row["currentQuantity"],
                                        )
                                        if new_weighting_status:
                                            count += 1
                                    except:
                                        print("ERROR with row ...")
                                if count > 0:
                                    print("Created %s rows" % count)
                            else:
                                print("No rows in %s..." % one_doc["name"])
                        else:
                            print("Document %s already exist..." % one_doc["name"])
                        print("Document %s finished..." % one_doc["name"])
                        print()
                    else:
                        print("Document %s skipping..." % one_doc["name"])
                        print()
            else:
                pass
                print("No docs to works!")
        else:
            print("No responce from server...")
        elapsed = time.time() - start
        print("%s - Upload docs finished!" % get_now())
        print("Elapsed %s seconds..." % elapsed)
        print()

    except requests.exceptions.ConnectionError:
        print("API Server connection error!")


@task(schedule=300)
def upload_decl_new():
    print("%s  -  Upload declared batches running!" % get_now())
    try:
        ip = settings.GLOBAL_SETTINGS["API_SERVER_URL"]
        request_prefix = "http://"
        request_postfix = "/MobileSMARTS/api/v1/Tables/Batches"
        request_txt = request_prefix + ip + request_postfix
        response = requests.get(request_txt)
        status = response.status_code
        count = 0
        if status == 200:
            print("%s - 200 Request OK!" % get_now())
            data = response.json()
            table_rows = data
            start = time.time()
            for one_row in table_rows["value"]:
                exist_rows = Declared_Batches.objects.all()
                if exist_rows.filter(
                    batch_pr__batch_name=one_row["batch"],
                    material__code=one_row["code"],
                    decl_quant=one_row["quant"],
                ).exists():
                    pass
                else:
                    try:
                        (
                            new_batch_obj,
                            new_batch_status,
                        ) = Batch_pr.objects.get_or_create(batch_name=one_row["batch"],)
                        if new_batch_status:
                            print("Created batch %s..." % one_row["batch"])
                    except:
                        print("ERROR with %s!" % one_row["batch"])
                    try:
                        new_material_obj = Material.objects.get(code=one_row["code"],)
                    except Material.DoesNotExist:
                        new_material_obj = Material(
                            code=one_row["code"], material_name=one_row["name"],
                        )
                        new_material_obj.save()
                        print(
                            "Created new material %s %s"
                            % (one_row["code"], one_row["name"])
                        )
                    except:
                        print("ERROR with %s %s!" % (one_row["code"], one_row["name"]))
                    new_declared_batches_obj = Declared_Batches(
                        batch_pr=new_batch_obj,
                        material=new_material_obj,
                        decl_quant=one_row["quant"],
                    )
                    new_declared_batches_obj.save()
                    count += 1
        else:
            print("No responce from server...")
        if count > 0:
            print("Created %s rows..." % count)
        else:
            print("No rows created...")
        elapsed = time.time() - start
        print("%s - Upload declared batches finished!" % get_now())
        print("Elapsed %s seconds..." % elapsed)
    except requests.exceptions.ConnectionError:
        print("API Server connection error!")
