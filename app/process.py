import os
import gzip
import shutil
from pathlib import Path

def decompress_files(data_dir: Path):
    for file in data_dir.glob("*.Z") + data_dir.glob("*.z"):
        with gzip.open(file, 'rb') as f_in:
            with open(file.with_suffix(''), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(file)

def convert_crx_to_rnx(data_dir: Path):
    for crx_file in data_dir.glob("*.crx"):
        os.system(f"crx2rnx {crx_file}")
        os.remove(crx_file)

