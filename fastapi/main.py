# data_downloader/downloading_files.py
import os
from datetime import datetime

def download_files():
    today = datetime.today().strftime('%Y-%m-%d')

    satellite_data = {
        "ANTC00CHL": "ANTC00CHL_R_20241680000_01D_30S_MO.rnx",
        "AREG00PER": "AREG00PER_R_20241680000_01D_30S_MO.rnx",
        "AREQ00PER": "AREQ00PER_R_20241680000_01D_30S_MO.rnx",
        "ASCG00SHN": "ASCG00SHN_R_20241680000_01D_30S_MO.rnx",
        "BAKE00CAN": "BAKE00CAN_R_20241680000_01D_30S_MO.rnx",
    }

    for satellite_name, file_name in satellite_data.items():
        directory_path = f"data_downloader/{today}/{satellite_name}"
        os.makedirs(directory_path, exist_ok=True)
        with open(os.path.join(directory_path, file_name), 'w') as f:
            f.write("Example file content")

if __name__ == "__main__":
    download_files()
