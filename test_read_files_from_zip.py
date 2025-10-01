import os
import pypdf, openpyxl, csv
from zipfile import ZipFile
import pytest
from io import TextIOWrapper


CURRENT_DIR = os.getcwd()
RESOURCES_DIR = os.path.join(CURRENT_DIR, 'resources')
ZIP_FILE = os.path.join(RESOURCES_DIR, 'archive.zip')


@pytest.fixture(scope="module", autouse=True)
def create_archive():
    if not os.path.exists(RESOURCES_DIR):
        os.mkdir(RESOURCES_DIR)

    files = [f for f in os.listdir(RESOURCES_DIR) if f.lower().endswith(('.pdf', '.xlsx', '.csv'))]

    with ZipFile(ZIP_FILE, 'w') as zf:
        for file in files:
            add_file = os.path.join(RESOURCES_DIR, file)
            zf.write(add_file, arcname=file)

    yield

    if os.path.exists(ZIP_FILE):
        os.remove(ZIP_FILE)


def test_csv_in_archive():
    with ZipFile(ZIP_FILE) as zip_file: # открываем архив
        with zip_file.open('csv_file.csv') as csv_file: # открываем файл в архиве
            csvreader = list(csv.reader(TextIOWrapper(csv_file, 'utf-8-sig'), delimiter=';')) # читаем содержимое файла и преобразуем его в список и декодируем его если в файле есть символы не из английского алфавита
            second_row = csvreader[1] # получаем вторую строку

            assert second_row[0] == 'Row A2' # проверка значения элемента в первом столбце второй строки
            assert second_row[1] == 'Row B2' # проверка значения элемента во втором столбце второй строки
