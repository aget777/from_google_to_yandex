#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import requests
from io import BytesIO
import os

import config
from parse_functions import *
from yandex_disk_func import *
from google_connector import *


# In[ ]:


path = config.path
dashboadr_folder = config.dashboadr_folder
yandex_token = config.yandex_token
# указываем путь к основной папке, в которой храняться папки с флайтами
main_folder = config.main_folder # путь к папке в формате /tmp


# In[ ]:


# функция добавляет ИД документа к базовому УРЛ гугла
# функция, чтобы забрать из ссылки гугл докс ИД
# ИД находится между определенными паттернами
# на выходе возвращаем строку с ИД
def get_data_from_sheet(base_link):
    # # стандартный УРЛ от гугла, в который нужно подставить ИД файла для скачивания
    url = config.url #'https://docs.google.com/spreadsheets/export?exportFormat=xlsx&id='
    start_index = str(base_link).find('/d/')
    end_index = str(base_link).find('/edit?')
    spreadsheetId = base_link[start_index+3:end_index]
    
    # spreadsheetId = get_sheet_id(base_link)
    # добавляем к стандартной ссылке гугл этот ИД
    final_url = url + spreadsheetId
    res = requests.get(final_url)
    
    return BytesIO(res.content)


# In[ ]:


# создаем функцию для подготовки места на Яндекс диске для загрузки файлов
# у нас есть 2 типа файлов - файлы excel и файлы pbi
# файлы excel мы просто загружаем в папку Клиента
# файлы pbi мы загружаем в папку Файлы дашбордов, которая находится внутри папки Клинета
# для того, чтобы отличить, какой файл куда следует загрузить функция на входе принимаетс специальный флаг для дашбордов flag='dashboard'
# для файлов excel никаких флашов не используем
# на входе фенкция принимает
# main_folder - путь к основной папке на Яндекс Диске, в которой хранятся папки клиентов - /tmp
# base_link - ссылка на гугл файл (либо эксель документ, либо гугл папка)
# name - название клиента
# report - название файла
def get_files_to_yandex_disk(base_link, name, report, flag):
    
    if flag=='dashboard':
        name = name + '/'
        # создаем путь к папке Дашборов внутри каждого клиента
        dashboadr_folder_path = os.path.join(path, dashboadr_folder)
        # прописываем путь к файлу дашборда, который сохранен на локальном компе
        content = os.path.join(dashboadr_folder_path, report)
        file_name = report
        name = name + dashboadr_folder
        # создаем конечный путь для каждого файла дашбордов
        file_path = name  +  dashboadr_folder + '/' + report
        # если на яндекс диске в папке дашбордов есть одноименный файл, то удаляем его
        delete_yandex_disk_file(file_path)       
        # открываем локально сохраненный файл дашборда и отправляем его на загрузку на яндекс диск
        with open(content, 'rb') as f:
            try:
                upload_file_to_yandex_disk(name, file_name, f)
            except:
                print('Ошибка при загрузке файла')
    if flag=='xlsx':
        # если мы загружаеем excel Файл, то сначала забираем из гугл ссылки ИД файла для загрузки
        spreadsheetId = get_sheet_id(base_link)
        # передаем ИД файла в нашу функцию для получения файла целиком (т.к. это excel получаем все единиым куском со всеми листами внутри)
        content = download_google_data(spreadsheetId)
        file_name = report + '.xlsx'
        file_path = name + file_name
        # если на яндекс диске в папке Клиента есть одноименный excel файл, то удаляем его
        delete_yandex_disk_file(file_path)
        # загружаем файл на яндекс диск в папку соответствующего клиента
        upload_file_to_yandex_disk(name, file_name, content)


# In[ ]:


# def get_data_to_yandex_disk(main_folder, base_link, name, report, yandex_token):
#     spreadsheetId = get_sheet_id(base_link)
#     content = download_google_data(spreadsheetId)
    
#     file_path = name + '/' + report + '.xlsx'
#     delete_yandex_disk_file(main_folder, file_path, yandex_token)
    
#     upload_file_to_yandex_disk(main_folder, name, report, content, yandex_token)


# In[ ]:


def get_dashboards_folder(dashboadr_folder):
    # проверяем - существует папка для временного сохранения файлов или нет
    # если ее нет, то создаем
    # если папка существует, то проверяем в ней наличие файлов
    # если файлы в ней есть, то очищаем папку от содержимого
    # в самом конце выполняем загрузку файлов из гугл диска
    
    # получаем адрес текущей папки
    directory = config.path
    current_directory = os.path.join(directory, dashboadr_folder)
    if dashboadr_folder not in list(os.listdir(directory)):
        os.makedirs(current_directory) # создаем папку для сохранения файлов дашбордов
    else:
        current_files_list = list(os.listdir(os.path.join(directory, dashboadr_folder)))
        if len(current_files_list)!=0:
            for file in current_files_list:
                os.remove(os.path.join(current_directory, file))
    return current_directory

