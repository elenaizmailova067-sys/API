import yadisk
import json
import requests
import time
from tqdm import tqdm
from urllib.parse import quote

def run_backup():
    # 1. Входные данные
    group_name = "PY-144" # Название вашей группы
    cat_text = input("Введите текст для картинки котика: ")
    token = input("Введите ваш токен Яндекс.Диска: ").strip()

    # Ссылка на картинку котика (CATAAS)
    cat_api_url = f"https://cataas.com{quote(cat_text)}"

    # Инициализация клиента Яндекс.Диска
    y = yadisk.YaDisk(token=token)

    # 2. Проверка токена
    if not y.check_token():
        print("Ошибка: Токен недействителен!")
        return

    # 3. Создание папки (Задание п.2)
    try:
        if not y.exists(group_name):
            y.mkdir(group_name)
            print(f"Папка '{group_name}' создана.")
        else:
            print(f"Папка '{group_name}' уже существует.")
    except Exception as e:
        print(f"Ошибка при работе с папкой: {e}")
        return

    # 4. Загрузка "по воздуху" (Задание п.1, п.3)
    log_data = []
    print("Начинаю загрузку...")

    # Текст картинки становится названием файла
    file_path = f"{group_name}/{cat_text}.jpg"

    # Используем tqdm для прогресс-бара (Задание п.4 обязательных требований)
    for _ in tqdm(range(1), desc="Загрузка на Я.Диск"):
        try:
            # Загрузка по URL без сохранения локально
            y.upload_url(cat_api_url, file_path)

            # Ждем, пока Яндекс скачает файл (до 30 секунд)
            # Это решит проблему 'Asynchronous operation failed'
            while True:
                status = y.get_operation_status(operation.operation_id)
                if status.status == "success":
                    break
                elif status.status == "failed":
                    raise Exception("Яндекс не смог скачать файл по ссылке")
                time.sleep(1) # Ждем секунду перед следующей проверкой

            # 5. Получение информации о файле для JSON (Задание п.4)
            meta = y.get_meta(file_path)
            log_data.append({
                "file_name": f"{cat_text}.jpg",
                "size": meta.size
            })
        except Exception as e:
            print(f"\nОшибка при загрузке файла: {e}")

    # 6. Сохранение JSON-отчета (Выходные данные п.1)
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=4)

    print(f"\nГотово! Результат сохранен в 'result.json' и в папке '{group_name}' на Диске.")

if __name__ == "__main__":
    run_backup()
