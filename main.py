import requests
import json
import time
from tqdm import tqdm
from urllib.parse import quote

class CatToYandex:
    def __init__(self, ya_token):
        self.ya_token = ya_token
        # Базовый домен API
        self.host = "https://cloud-api.yandex.net"
        self.headers = {
            'Authorization': f'OAuth {self.ya_token}',
            'Content-Type': 'application/json'
        }

    def create_folder(self, folder_name):
        """Создает папку: PUT /v1/disk/resources"""
        url = f"{self.host}/v1/disk/resources"
        params = {'path': folder_name}
        response = requests.put(url, headers=self.headers, params=params)

        if response.status_code == 201:
            print(f"Папка '{folder_name}' создана.")
        elif response.status_code == 409:
            print(f"Папка '{folder_name}' уже существует.")
        else:
            print(f"Ошибка {response.status_code}: {response.json().get('message')}")

    def upload_by_url(self, folder_name, file_url, file_name):
        """Загрузка по ссылке: POST /v1/disk/resources/upload"""
        url = f"{self.host}/v1/disk/resources/upload"
        params = {
            'path': f"{folder_name}/{file_name}.jpg",
            'url': file_url
        }
        response = requests.post(url, headers=self.headers, params=params)
        return response.status_code

    def get_file_info(self, folder_name, file_name):
        """Метаданные: GET /v1/disk/resources"""
        url = f"{self.host}/v1/disk/resources"
        params = {'path': f"{folder_name}/{file_name}.jpg"}

        # Ждем чуть дольше, чтобы Яндекс успел скачать файл к себе
        time.sleep(2)
        res = requests.get(url, headers=self.headers, params=params).json()
        return {"file_name": f"{file_name}.jpg", "size": res.get('size', 'unknown')}

def run_backup():
    group_name = "PY-144"
    cat_text = input("Введите текст для картинки котика: ")
    token = input("Введите ваш токен Яндекс.Диска: ")

    # Важно: URL должен вести прямо на файл изображения
    cat_image_url = f"https://cataas.com{quote(cat_text)}"

    uploader = CatToYandex(token)

    # 1. Создаем папку
    uploader.create_folder(group_name)

    # 2. Загружаем
    log_data = []
    print("Начинаю загрузку...")

    for _ in tqdm(range(1), desc="Загрузка на Я.Диск"):
        status = uploader.upload_by_url(group_name, cat_image_url, cat_text)

        if status == 202:
            info = uploader.get_file_info(group_name, cat_text)
            log_data.append(info)
        else:
            print(f"\nОшибка загрузки {status}")

    # 3. Сохраняем отчет
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=4)

    print("\nГотово! Результат в result.json")

if __name__ == "__main__":
    run_backup()

