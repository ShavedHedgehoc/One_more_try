import random
import time
import os
import csv
import openpyxl
from openpyxl import load_workbook
from random import randint


def get_batch():
    month_list = [m for m in "ABCDEFGHIJKL"]
    year_list = [8, 9]
    batch_number = randint(1, 1000)
    month = random.choice(month_list)
    year = random.choice(year_list)
    batch = str(batch_number) + month + str(year)
    return batch


def get_terminal_name():
    terminal_list = ["122", "121", "202", "201", "302", "301"]
    terminal_name = random.choice(terminal_list)
    return terminal_name


def get_can_name():
    cur_time = time.strftime("%d%m%Y%H%M%S", time.localtime())
    can_name = "".join(["987", cur_time, get_terminal_name()])
    return can_name


def get_doc_name():
    cur_time = time.strftime("%d.%m.%Y_%H.%M.%S", time.localtime())
    doc_name = "_".join(["Взвешивание", cur_time, get_terminal_name()])
    return doc_name


if __name__ == "__main__":
    doc_name = get_doc_name()
    user_list = []
    product_list = []
    user_file = "./Пользователи.csv"
    #product_file = "Номенклатура.csv"
    product_file = "output.csv"
    report_file = doc_name + ".csv"
    with open(user_file, "r", encoding="utf-8") as users:
        reader = csv.reader(users)
        next(reader, None)
        for row in reader:
            user_list.append(row)
        users.close
    with open(product_file, "r", encoding="utf-8") as products:
        reader = csv.reader(products)
        next(reader, None)
        for row in reader:
            product_list.append(row)
        products.close
    rows_list = []
    rows_quantity = randint(1, 10)
    for row_number in range(1, rows_quantity):
        product = random.choice(product_list)
        #r_lot = "00031209641412201802"
        single_row = [
            product[0].split(";")[2].strip(" "),  # Сюда вставить стрип
            product[0].split(";")[3],
            0,
            randint(1, 2000),
            product[0].split(";")[0],
        ]
        rows_list.append(single_row)
    with open(report_file, "w", encoding="utf-8", newline="") as report:
        writer = csv.writer(report, delimiter=";")
        writer.writerow(["#{Document}"])
        writer.writerow(["Name;Varka;Vypolnil;ShtrihkodEmkosti;Apparat"])
        writer.writerow(
            [
                get_doc_name(),
                get_batch(),
                random.choice(user_list)[0].split(";")[0],
                get_can_name(),
                randint(1, 150),
            ]
        )
        writer.writerow(["#{DeclaredItems}"])
        writer.writerow(
            ["Productid;Product.Name;DeclaredQuantity;CurrentQuantity;Partiya"]
        )
        for row in rows_list:
            writer.writerow(row)
        writer.writerow(["#{CurrentItems}"])
        writer.writerow(
            ["Productid;Product.Name;DeclaredQuantity;CurrentQuantity;Partiya"]
        )
        for row in rows_list:
            writer.writerow(row)
        report.close

    # product_file = 'Номенклатура.csv'
    # wb = load_workbook('./Номенклатура.xlsx')
    # ws = wb['Лист1']
    # report_filename = 'output.csv'
    # with open(report_filename, 'w', encoding='utf-8', newline='') as csvfile:
    #     csv_file = csv.writer(csvfile, delimiter=';')
    #     for row in ws.values:
    #         csv_file.writerow(row)
    # print(get_can_name())
    # #df_files = read_xl_file('Номенклатура.xlsx')
    # full_list=[]
    # doc_header=["#{Document}","{Document.Варка}",'']
    # doc_header_value=["Загрузка12345",get_batch(),"",""]
    # full_list.append(doc_header)
    # full_list.append(doc_header_value)
    # report_filename = 'users2.csv'

    # with open(report_filename, 'w', encoding='utf-8', newline='') as csvfile:
    #     csv_file = csv.writer(csvfile, delimiter=';')
    #     for row in full_list:
    #         csv_file.writerow(row)
