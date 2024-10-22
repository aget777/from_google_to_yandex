import config
from downloader_script import *

# обычная ссылка на доступ к папке  из личного кабинета
public_key = config.public_key
# ссылка на основной файл гугл докс (на каждом лите отдельный клиент со ссылками на файлы с данными)
base_link = config.base_link
# название папки на Яндекс диске, в которой будут храниться дашборды
dashboadr_folder = config.dashboadr_folder

def main():
    get_data_to_yandex_disk(public_key, base_link, dashboadr_folder)

if __name__ == '__main__':
    main()


