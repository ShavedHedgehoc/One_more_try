import os
import string
import xlrd
import pandas as pd

#full_name = os.path.join(file_path, file_name)
# РАзобраться с паролем

if __name__ == '__main__':
    xl_file = {"Копия Отчет.xlsx",
               "Копия Отчет2.xlsx"}
    df_summary = None
    df_batch = None
    for one_file in xl_file:
        xl = pd.ExcelFile(one_file)
        sh = xl.sheet_names[0]
        df = pd.read_excel(xl, sheet_name=sh, header=None, dtype=str)
        cur_date = df.iloc[0, 14]
        df2 = df.dropna(subset=[8, 16])
        for index, row in df2.iterrows():
            if row[1] == "набор":
                set_batch = row[4]
            if pd.isna(row[1]):
                batch_row = pd.DataFrame([[set_batch, row[2], row[3], row[4]]],
                                         columns=['ПартияГП', 'КодНЗ', 'АртикулНЗ', 'ПартияНЗ'])
                df_batch = pd.concat(
                    [df_batch, batch_row], ignore_index=True)
            elif row[1] == "Код":
                pass
            else:
                summary_row = pd.DataFrame([[cur_date, row[0], row[3], row[4], row[8]]],
                                           columns=['Дата', 'Код', 'Артикул', 'Партия', 'Конвейер'])
                df_summary = pd.concat(
                    [df_summary, summary_row], ignore_index=True)
    df_summary.to_excel('Сводка2.xlsx', index=False, header=True)
    df_batch.to_excel('ПартииНаборов.xlsx', index=False, header=True)
    xl = pd.ExcelFile("Регламент.xlsx")
    sh = xl.sheet_names[0]
    df = pd.read_excel(xl, sheet_name=sh, header=None, dtype=str)
    df_res = None

    for index, row in df.iterrows():
        if (not(pd.isna(row[0]))
            and (row[0] != "ГП")
            and (row[0] != "999999")
            and (row[0] != "999000")
            and (row[0] != "код 1С")
            ):
            if str(row[7]).replace(" ","") == "-" or pd.isna(row[7]):
                ves_fazy_1_nom = 0
            else:
                ves_fazy_1_nom = row[7]
            if str(row[8]).replace(" ","") == "-" or pd.isna(row[8]):
                ves_fazy_1_min = 0
            else:
                ves_fazy_1_min = row[8]
            if str(row[9]).replace(" ","") == "-" or pd.isna(row[9]):
                ves_fazy_1_max = 0
            else:
                ves_fazy_1_max = row[9]
            if str(row[10]).replace(" ","") == "-" or pd.isna(row[10]):
                ves_fazy_2_nom = 0
            else:
                ves_fazy_2_nom = row[10]
            if str(row[11]).replace(" ","") == "-" or pd.isna(row[11]):
                ves_fazy_2_min = 0
            else:
                ves_fazy_2_min = row[11]
            if str(row[12]).replace(" ","") == "-" or pd.isna(row[12]):
                ves_fazy_2_max = 0
            else:
                ves_fazy_2_max = row[12]
            if (ves_fazy_1_nom == 0) and (ves_fazy_2_nom == 0):
                priznak_ves = "Нет"
            else:
                priznak_ves = "Да"
            if str(row[80]).replace(" ","") == "-" or pd.isna(row[80]):
                shablon_mark_1 = "-"
            else:
                shablon_mark_1 = row[80]
            if str(row[81]).replace(" ","") == "-" or pd.isna(row[81]):
                razmer_mark_1 = "-"
            else:
                razmer_mark_1 = row[81]
            if str(row[82]).replace(" ","") == "-" or pd.isna(row[82]):
                osob_mark_1 = "-"
            else:
                osob_mark_1 = row[82]
            if str(row[84]).replace(" ","") == "-" or pd.isna(row[84]):
                color_mark_1 = "-"
            else:
                color_mark_1 = row[84]
            if str(row[85]).replace(" ","") == "-" or pd.isna(row[85]):
                shablon_mark_2 = "-"
            else:
                shablon_mark_2 = row[85]
            if str(row[86]).replace(" ","") == "-" or pd.isna(row[86]):
                razmer_mark_2 = "-"
            else:
                razmer_mark_2 = row[86]
            if str(row[87]).replace(" ","") == "-" or pd.isna(row[87]):
                osob_mark_2 = "-"
            else:
                osob_mark_2 = row[87]
            if str(row[89]).replace(" ","") == "-" or pd.isna(row[89]):
                color_mark_2 = "-"
            else:
                color_mark_2 = row[89]
            if (shablon_mark_1 == "-") and (shablon_mark_2 == "-"):
                priznak_mark = "Нет"
            else:
                priznak_mark = "Да"
            if str(row[93]).replace(" ","") == "-" or pd.isna(row[93]):
                variant_etik = "-"
            else:
                variant_etik = row[93]
            if str(row[94]).replace(" ","") == "-" or pd.isna(row[94]):
                opis_etik = "-"
            else:
                opis_etik = row[94]
            if str(row[95]).replace(" ","") == "-" or pd.isna(row[95]):
                dop_etik = "-"
            else:
                dop_etik = row[95]
            if variant_etik == "-":
                priznak_etik = "Нет"
            else:
                priznak_etik = "Да"
            if str(row[100]).replace(" ","") == "-" or pd.isna(row[100]):
                variant_ukup = "-"
            else:
                variant_ukup = row[100]
            if str(row[101]).replace(" ","") == "-" or pd.isna(row[101]):
                sposob_ukup = "-"
            else:
                sposob_ukup = row[101]
            if str(row[102]).replace(" ","") == "-" or pd.isna(row[102]):
                result_ukup = "-"
            else:
                result_ukup = row[102]
            if variant_ukup == "-":
                priznak_ukup = "Нет"
            else:
                priznak_ukup = "Да"
            
            reg_row = pd.DataFrame(
                [[row[0],
                  row[1],
                  row[2],
                  priznak_ves,
                  ves_fazy_1_nom,
                  ves_fazy_1_min,
                  ves_fazy_1_max,
                  ves_fazy_2_nom,
                  ves_fazy_2_min,
                  ves_fazy_2_max,
                  priznak_mark,
                  shablon_mark_1,
                  razmer_mark_1,
                  osob_mark_1,
                  color_mark_1,
                  shablon_mark_2,
                  razmer_mark_2,
                  osob_mark_2,
                  color_mark_2,
                  priznak_etik,
                  variant_etik,
                  opis_etik,
                  dop_etik,
                  priznak_ukup,
                  variant_ukup,
                  sposob_ukup,
                  result_ukup
                  ]],
                columns=['Код',
                         'Артикул',
                         'Наименование',
                         'Признак_Вес',
                         'Вес_фазы_1_ном',
                         'Вес_фазы_1_мин',
                         'Вес_фазы_1_макс',
                         'Вес_фазы_2_ном',
                         'Вес_фазы_2_мин',
                         'Вес_фазы_2_макс',
                         'Признак_маркировка',
                         'Шаблон_маркировка_1',
                         'Размер_маркировка_1',
                         'Особенность_маркировка_1',
                         'Цвет_маркировка_1',
                         'Шаблон_маркировка_2',
                         'Размер_маркировка_2',
                         'Особенность_маркировка_2',
                         'Цвет_маркировка_2',
                         'Признак_этикеровка',
                         'Вариант_этикеровка',
                         'Описание_этикеровка',
                         'Дополнительно_этикеровка',
                         'Признак_укупорка',
                         'Вариант_укупорка',
                         'Способ_укупорка',
                         'Результат_укупорка'
                         ])
            df_res = pd.concat(
                [df_res, reg_row], ignore_index=True
            )
    df_res.to_excel('H2.xlsx', index=False, header=True)
