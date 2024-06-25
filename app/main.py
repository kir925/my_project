import threading
import time
from app.rinex_processor import start_daemons
from app.fastapi_server import start_fastapi
from app.user_app import start_user_application

def main():
    rinex_files = ["rinex_files/DAEJ00KOR_R_20240010000_01D_30S_MO.rnx"]  # Добавьте пути к вашим RINEX файлам
    start_daemons(rinex_files)

    fastapi_thread = threading.Thread(target=start_fastapi)
    fastapi_thread.start()

    user_thread = threading.Thread(target=start_user_application)
    user_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping application...")

if __name__ == "__main__":
    main()

