#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import requests
from io import BytesIO
import os
import yadisk
import gdown
import json

import config
from parse_functions import *
from yandex_disk_func import *
from google_connector import *

# основная функция для полного цикла перелива файлов из гугл диска на яндекс диск
def get_data_to_yandex_disk(public_key, base_link, dashboadr_folder):
    # забираем список папок в нужной нам директории
    res = get_yandex_disk_folders(public_key)
    yandex_folders = res.json() # парсим ответ

    # забираем данные из основной управленческой таблицы
    content = get_data_from_sheet(base_link)
    sheet_names = pd.ExcelFile(content)
    # если появился новый клиент
    # мы проверяем, что этого названия НЕТ среди папок на Яндекс Диске
    # созлаем папку Клиента
    # внутри нее создаем папку для файлов дашбордов
    
    folders_list = get_folder_name(yandex_folders['_embedded']['items'])
    for name in sheet_names.sheet_names:
        if name not in folders_list:
            print(name)
            dashboard_folder = '/' + name + '/' + dashboadr_folder
            create_yandex_disk_folder(name)
            create_yandex_disk_folder(dashboard_folder)


    # обновляем список папок на Яндекс диске
    res = get_yandex_disk_folders(public_key)
    yandex_folders = res.json() # парсим ответ

    # проходим через цикл по всем листам в управленческой таблице
    # вызываем функцию и забираем названия папок на яндекс диске
    folders_list = get_folder_name(yandex_folders['_embedded']['items'])
    
    for name in sheet_names.sheet_names:
        print(name)
        cols_range = 'A:B' # задаем диапазон полей, которые нам нужны
        df = pd.read_excel(content, sheet_name=name, usecols=cols_range, names=['report_name', 'report_link'])
        # нормализуем назания отчетов - приводим в нижний регистр, обрезаем по краям, избаляемся от технических символов(перенос строки и тд)
        df['report_name'] = df['report_name'].str.lower().str.strip().str.replace('\n', ' ')
        # создаем отдельный список с названиями отчетов и проодим по нему через цикл
        reports_list = list(df['report_name'])
        # запускаем блок парсинга отчетов
        for report in reports_list:
            # print(report)
            if report == 'файлы дашбордов':
                parse_info = df[df['report_name']==report].reset_index(drop=True)
                base_link = parse_info['report_link'][0]
                # print(base_link)
                # создаем папку для сохранения дашбордов, если ее нет
                # если она есть, то очищаем ее от файлов
                current_directory = get_dashboards_folder(dashboadr_folder)
                gdown.download_folder(base_link, output=current_directory, quiet=True, use_cookies=False)
                # получаем список файлов дашбордов
                current_files_list = list(os.listdir(current_directory))
                if len(current_files_list) > 0:
                    for report in current_files_list:
                        get_files_to_yandex_disk(base_link, name, report, flag='dashboard')
                        
                get_dashboards_folder(dashboadr_folder)

            else:
                parse_info = df[df['report_name']==report].reset_index(drop=True)
                base_link = parse_info['report_link'][0]
                get_files_to_yandex_disk(base_link, name, report, flag='xlsx')

