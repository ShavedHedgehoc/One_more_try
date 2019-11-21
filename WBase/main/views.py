import requests
import json
import time
from django.shortcuts import render
from .models import Material

# Create your views here.

def get_products(): 
    start=time.time()   
    try:
        response = requests.get("http://srv-webts:9504/MobileSMARTS/api/v1/Products")
        data = response.json()
        for one_record in data['value']:
            material, _ =Material.objects.get_or_create(
                code = one_record['id'],
                marking=one_record['marking'],
                material_name = one_record['name'],
                unit = one_record['packings'][0]['name'],                
                )            
    except:
         print("Ошибка",one_record['name'], "_"+one_record['packings'][0]['barcode']+"_")

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
    
    return time.time()-start


def get_documents_list():
    try:
        response = requests.get(            
            "http://srv-webts:9504/MobileSMARTS/api/v1/Docs/Vzveshivanie?$count=true")
        data = response.json()
        quant = data['@odata.count']
        #if quant>0:
            
    except:
        pass
    return get_data

def get_document_rows(doc_id):
    try:
        request_prefix="http://srv-webts:9504/MobileSMARTS/api/v1/Docs('"
        request_postfix=")/declaredItems?$expand=product"
        request_full=request_prefix+doc_id+request_postfix
        response = requests.get(request_full)            
        get_data = response.json()
    except:
        pass
    return get_data

   


def get_documents_quant():
    try:
        response = requests.get(
            "http://srv-webts:9504/MobileSMARTS/api/v1/Docs/Vzveshivanie?$select=none&$count=true")
        data = response.json()
        quant = data['@odata.count']
    except:
        quant = "Server not found"
    return quant

def delete_document(doc_id):
    request_prefix="http://srv-webts:9504/MobileSMARTS/api/v1/Docs('"
    request_postfix=")"
    request_full=request_prefix+doc_id+request_postfix
    requests.delete(request_full)
    return

def index(request):
    product_list=get_products()
    return render(request, 'index.html',{'list':product_list})


def index2(request):
    product_list=get_products()
    
    


    
    docs_list = get_documents_list()
    sss=[]
    for one_doc in docs_list['value']:
        #sss.append(one_doc)
        lll=get_document_rows(one_doc['id'])
        for one_row in lll['value']:
            d=[one_doc['ShtrihkodEmkosti'],one_row['product']['id'],one_row['product']['name'],one_row['currentQuantity']]
            sss.append(d)
     #   if 

    #    delete_document(one_doc['id'])        
    #     request_prefix="http://srv-webts:9504/MobileSMARTS/api/v1/Docs('"
    #     request_postfix=")"
    #     request_full=request_prefix+one_doc['id']+request_postfix
    #     responce=requests.delete(request_full)


    return render(request, 'index.html',{'list':product_list})
