import os
import xlrd
import pandas as pd

#full_name = os.path.join(file_path, file_name)
# РАзобраться с паролем

if __name__ == '__main__':
    xl_file = {"Копия Отчет.xlsx",
               "Копия Отчет2.xlsx"}
    for one_file in xl_file:
        xl = pd.ExcelFile(one_file)
        sh = xl.sheet_names[0]
        df = pd.read_excel(xl, sheet_name=sh, header=None, dtype=str)
        cur_date = df.iloc[0, 14]
        df2 = df.dropna(subset=[8, 16])
        for index, row in df2.iterrows():
            if row[1] == "набор":
                set_batch = row[4]
            if pd.isna(row[0]):
                print("Набор %s, %s, %s, %s" %
                      (set_batch, row[2], row[3], row[4]))
