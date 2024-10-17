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


def get_data_to_yandex_disk(main_folder, base_link, name, report, yandex_token):
    spreadsheetId = get_sheet_id(base_link)
    content = download_google_data(spreadsheetId)
    
    file_path = name + '/' + report + '.xlsx'
    delete_yandex_disk_file(main_folder, file_path, yandex_token)
    
    upload_file_to_yandex_disk(main_folder, name, report, content, yandex_token)

