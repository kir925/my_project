import os
import time
import subprocess
from datetime import datetime, timedelta
from data_processing.download_data import download_data
from data_processing.process_data import process_files

def main():
    while True:
        # Вычисление даты 5 дней назад
        date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        
        # Шаг 1: Загрузка данных
        print(f"Downloading data for date: {date}")
        download_data(date)
        
        # Предполагается, что загруженный файл сохранён в текущей директории
        zip_file = f"{date}.zip"
        extract_dir = f"{date}_extracted"
        
        # Шаг 2: Извлечение данных
        print(f"Extracting {zip_file}")
        os.makedirs(extract_dir, exist_ok=True)
        subprocess.run(["unzip", "-o", zip_file, "-d", extract_dir])
        
        # Шаг 3: Обработка данных
        print(f"Processing files in {extract_dir}")
        process_files(extract_dir)
        
        # Шаг 4: Запуск публикации данных для каждого RINEX файла
        for filename in os.listdir(extract_dir):
            if filename.endswith(".rnx"):
                file_path = os.path.join(extract_dir, filename)
                print(f"Starting publisher for {file_path}")
                subprocess.Popen(["python3", "data_emulation/publisher.py", file_path])
        
        # Ожидание до следующего запуска в 22:00 следующего дня
        now = datetime.now()
        next_run = now.replace(hour=22, minute=0, second=0, microsecond=0) + timedelta(days=1)
        sleep_seconds = (next_run - now).total_seconds()
        print(f"Sleeping for {sleep_seconds / 3600:.2f} hours")
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    main()

