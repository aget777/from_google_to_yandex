#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os



# google links
# стандартный УРЛ от гугла, в который нужно подставить ИД файла для скачивания
url = 'https://docs.google.com/spreadsheets/export?exportFormat=xlsx&id='
# ссылка на основной файл гугл докс (на каждом лите отдельный клиент со ссылками на файлы с данными)
base_link = 'https://docs.google.com/spreadsheets/d/1M6CdeQ8b_Uf5lXWqrxLRAX9-EP3SyIfi0rJfiAMbkEY/edit?usp=sharing'

# yandex links
token_path = r'C:\Users\o.bogomolov\Desktop\Jupyter_notebook\34_03_download_files_from_google_to_yandex\cred'
token_name = 'yandex_token.txt'

yandex_token = open(os.path.join(token_path, token_name), encoding='utf-8').read()

# указываем путь к основной папке, в которой храняться папки с флайтами
main_folder = '/tmp'
public_key = 'https://disk.yandex.ru/d/Fm8-4DnCb5J18w' # обычная ссылка на доступ к папке одного данного ФЛАЙТА из личного кабинета

