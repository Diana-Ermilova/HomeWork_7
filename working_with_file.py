import csv
import os
import io
from socket import create_server
from zipfile import ZipFile
import pytest
from openpyxl.reader.excel import load_workbook
from pypdf import PdfReader

PATH_RES ="resources"
PATH_ARCH = "my_zip.zip"

L_files = os.listdir(PATH_RES) #создаем список для удобства
print(L_files) #для дебага и собственного спокойствия

def create_archive(): #создаем архив с файлами
    with ZipFile(PATH_ARCH, mode="w") as myzip:
        for file in L_files:
            myzip.write(os.path.join(PATH_RES, file)) #файлы вынулись из директории и из них создался архив
#create_archive()

#читаем файлы
def test_reading_from_archive():
    with ZipFile(PATH_ARCH, mode="r") as myzip:
        for file in myzip.namelist():
            if file.endswith(".csv"):
                with io.TextIOWrapper(myzip.open(file, "r"), encoding="utf-8") as io_wrapper:
                    csvfile = csv.reader(io_wrapper)
                    for row in csvfile:
                        print(row)
                        if row == ['3', 'Sarena', 'Cornewell', 'scornewell2@nyu.edu', 'Female', '251.107.184.114']: #проверка наличия строки
                            break
                    else:
                        raise Exception('Row not found')
            elif file.endswith(".xlsx"):
                with myzip.open(file, "r")  as io_xlsx:
                    xlsxfile = load_workbook(io_xlsx)
                    sheet = xlsxfile.active
                    assert sheet.cell(row=1, column=1).value == 'snail!'
                    #sheet = xlsxfile.active

            elif file.endswith("pdf"):
                with myzip.open(file, "r") as reader:
                    print(type(reader))
                    pdf_file = PdfReader(reader)
                    page = pdf_file.pages[0]
                    text = page.extract_text()
                    print(text)
                    assert "Никакой полезной информации он не несёт" in text
#reading_from_archive()
#проверки
#PdfReader(open("resources/very_important.pdf", "b+r")) #это было для дебага