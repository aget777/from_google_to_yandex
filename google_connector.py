#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import io
import os
import config


# In[ ]:


# стандартный УРЛ от гугла, в который нужно подставить ИД файла для скачивания
url_export_xlsx = 'https://docs.google.com/spreadsheets/export?exportFormat=xlsx&id='


# In[ ]:


# функция для того, чтобы создать подключение к Гугл докс
def create_connection(service_file):
    client = None
    scope = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
    ]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            service_file, scope
        )
        client = gspread.authorize(credentials)
        print("Connection established successfully...")
    except Exception as e:
        print(e)
    return client


# In[ ]:


# функция для загрузки данных в гугл таблицу
def export_dataframe_to_google_sheet(worksheet, df):
    try:
        worksheet.update(
            [df.columns.values.tolist()] + df.values.tolist(),
            
        )
        print("DataFrame exported successfully...")
    except Exception as e:
        print(e)


# In[ ]:


# функция забираем ИД документа из УРЛ гугла
# на выходе возвращаем ИД
def get_sheet_id(base_link):
    # # стандартный УРЛ от гугла, в который нужно подставить ИД файла для скачивания
    url = config.url #'https://docs.google.com/spreadsheets/export?exportFormat=xlsx&id='
    start_index = str(base_link).find('/d/')
    end_index = str(base_link).find('/edit?')
    spreadsheetId = base_link[start_index+3:end_index]
    
    return spreadsheetId


# In[ ]:


# функция для получения содержимого из гугл файла
# она НЕ сохраняет этот файл на диск
# она возвращает данные, которые мы можем дальше отправить в Облако или сохранить локально
def download_google_data(spreadsheetId):
    response = requests.get(f'https://docs.google.com/spreadsheets/d/{spreadsheetId}/export?format=xlsx')
    content = response.content
    
    return content

