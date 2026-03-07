import requests
import json
from tqdm import tqdm
from settings import yd_token

class CatToYandex:
    def __init__(self, ya_token):
        self.ya_token = ya_token
        self.base_url = "https://cloud-api.yandex.net"
        self.headers = {
            'Authorization': f'OAuth {self.ya_token}',
            'Content-Type': 'application/json'
        }

    def create_folder(self, folder_name):
        """Создает папку на Яндекс.Диске."""
        params = {'path': folder_name}
        response = requests.put(self.base_url, headers=self.headers, params=params)
        if response.status_code == 201:
            print(f"Папка '{folder_name}' создана.")
        elif response.status_code == 409:
            print(f"Папка '{folder_name}' уже существует.")

    def upload_by_url(self, folder_name, file_url, file_name):
        """Загружает файл на Диск 'по воздуху' через URL."""
        upload_url = f"{self.base_url}/upload"
        params = {
            'path': f"{folder_name}/{file_name}.jpg",
            'url': file_url
        }
        response = requests.post(upload_url, headers=self.headers, params=params)
        return response.status_code

    def get_file_info(self, folder_name, file_name):
        """Получает метаданные файла для JSON-отчета."""
        params = {'path': f"{folder_name}/{file_name}.jpg"}
        res = requests.get(self.base_url, headers=self.headers, params=params).json()
        return {"file_name": f"{file_name}.jpg", "size": res.get('size', 'unknown')}

def run_backup():
    # Входные данные
    group_name = "PY-144"  # Название вашей группы
    cat_text = input("Введите текст для картинки котика: ")
    token = input("Введите ваш токен Яндекс.Диска: ")

    cat_api_url = f"https://cataas.com{cat_text}"
    uploader = CatToYandex(token)

    # 1. Создаем папку
    uploader.create_folder(group_name)

    # 2. Загружаем и отслеживаем прогресс
    log_data = []
    print("Начинаю загрузку...")

    # Используем tqdm для визуализации (имитируем процесс для 1 файла)
    for _ in tqdm(range(1), desc="Загрузка на Я.Диск"):
        status = uploader.upload_by_url(group_name, cat_api_url, cat_text)
        if status == 202:
            info = uploader.get_file_info(group_name, cat_text)
            log_data.append(info)

    # 3. Сохраняем JSON-отчет
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=4)

    print("\nГотово! Информация сохранена в result.json")

if __name__ == "__main__":
    run_backup()
