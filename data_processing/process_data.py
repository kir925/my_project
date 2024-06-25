import os
import zipfile
import gzip
import shutil
import subprocess

def extract_file(file_path, extract_dir):
    _, extension = os.path.splitext(file_path)
    extracted_files = []
    if extension in ['.zip']:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            extracted_files = zip_ref.namelist()
    elif extension in ['.gz']:
        output_file = os.path.join(extract_dir, os.path.basename(file_path).replace('.gz', ''))
        with gzip.open(file_path, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        extracted_files = [output_file]
    elif extension in ['.z', '.Z']:
        output_file = os.path.join(extract_dir, os.path.basename(file_path).replace('.z', '').replace('.Z', ''))
        with open(file_path, 'rb') as f_in, open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        extracted_files = [output_file]

    # Remove the original file after extraction
    if extracted_files:
        os.remove(file_path)

    return extracted_files

def extract_nested_files(archive_file, extract_dir):
    os.makedirs(extract_dir, exist_ok=True)
    files_to_process = [archive_file]

    while files_to_process:
        current_file = files_to_process.pop(0)
        extracted_files = extract_file(current_file, extract_dir)
        for extracted_file in extracted_files:
            if extracted_file.endswith(('.zip', '.gz', '.z', '.Z')):
                files_to_process.append(os.path.join(extract_dir, extracted_file))

def process_files(extract_dir, rnx_dir):
    os.makedirs(rnx_dir, exist_ok=True)
    for root, dirs, files in os.walk(extract_dir):
        for filename in files:
            if filename.endswith(".crx"):
                crx_file = os.path.join(root, filename)
                rnx_file = os.path.join(rnx_dir, filename.replace(".crx", ".rnx"))
                print(f"Converting {crx_file} to {rnx_file}")
                subprocess.run(["crx2rnx", crx_file, rnx_file, "-f"])
            elif filename.endswith(".24d"):
                d_file = os.path.join(root, filename)
                o_file = os.path.join(rnx_dir, filename.replace(".24d", ".24o"))
                print(f"Converting {d_file} to {o_file}")
                subprocess.run(["crx2rnx", d_file, o_file, "-f"])

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process RINEX files.")
    parser.add_argument("--archive_file", type=str, default='zip/2024-01-01.zip',
                        help="Path to the archive file containing RINEX data.")
    parser.add_argument("--extract_dir", type=str, default='extracted_data',
                        help="Directory where extracted files will be saved.")
    parser.add_argument("--rnx_dir", type=str, default='rnx_files',
                        help="Directory where processed .rnx and .24o files will be saved.")
    
    args = parser.parse_args()

    # Распаковка вложенных сжатых файлов из архива
    extract_nested_files(args.archive_file, args.extract_dir)

    # Обработка файлов .crx и .24d в распакованной директории
    process_files(args.extract_dir, args.rnx_dir)
