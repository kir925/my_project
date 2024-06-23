import requests
from pathlib import Path

BASE_URL = "https://api.simurg.space/datafiles/map_files"

def download_file(date: str, data_dir: Path) -> Path:
    url = f"{BASE_URL}?date={date}"
    local_zip_path = data_dir / f"{date}.zip"
    
    if local_zip_path.exists():
        return data_dir
    
    response = requests.get(url, stream=True)
    total_length = response.headers.get('content-length')

    with open(local_zip_path, "wb") as f:
        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)

    with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
        zip_ref.extractall(data_dir)

    return data_dir

