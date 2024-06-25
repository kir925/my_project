import os
import subprocess
from datetime import datetime, timedelta
from data_processing.download_data import download_data
from data_processing.process_data import process_files
from data_emulation.publisher import publish_data

def main():
    while True:
        date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        
        print(f"Downloading data for date: {date}")
        download_data(date, 'downloads')
        
        archive_file = f"downloads/{date}.zip"
        extract_dir = f"{date}_extracted"
        
        print(f"Extracting {archive_file}")
        os.makedirs(extract_dir, exist_ok=True)
        extract_file(archive_file, extract_dir)
        
        print(f"Processing files in {extract_dir}")
        process_files(extract_dir)
        
        for filename in os.listdir(extract_dir):
            if filename.endswith(".rnx"):
                file_path = os.path.join(extract_dir, filename)
                print(f"Publishing data from {file_path}")
                publish_data(file_path)
        
        # Спим до следующего дня
        next_run = datetime.now().replace(hour=22, minute=0, second=0, microsecond=0) + timedelta(days=1)
        sleep_seconds = (next_run - datetime.now()).total_seconds()
        print(f"Sleeping for {sleep_seconds / 3600:.2f} hours")
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    main()
