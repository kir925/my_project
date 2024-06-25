import schedule
import time
import requests
import os
from datetime import datetime, timedelta

def download_data(date, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    file_name = os.path.join(save_dir, f"{date}.zip")
    with open(file_name, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                sys.stdout.flush()

def job():
    # Вычисляем дату 5 дней назад от текущего момента времени
    date_5_days_ago = datetime.now() - timedelta(days=5)
    date = date_5_days_ago.strftime("%Y-%m-%d")
    save_dir = 'downloads'

    download_data(date, save_dir)

if __name__ == "__main__":
    # Запускаем задачу каждый день в 22:00
    schedule.every().day.at("22:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Проверяем расписание каждую минуту
