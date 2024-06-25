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


def find_latest_zip(directory):
    downloads_dir = os.path.join(directory, 'downloads')
    zip_files = [f for f in os.listdir(downloads_dir) if f.endswith('.zip')]
    if zip_files:
        latest_zip = max(zip_files, key=lambda f: os.path.getctime(os.path.join(downloads_dir, f)))
        return os.path.join(downloads_dir, latest_zip)
    else:
        return None


def extract_nested_files(archive_file, extract_dir):
    os.makedirs(extract_dir, exist_ok=True)
    files_to_process = [archive_file]

    while files_to_process:
        current_file = files_to_process.pop(0)
        extracted_files = extract_file(current_file, extract_dir)
        for extracted_file in extracted_files:
            if extracted_file.endswith(('.zip', '.gz', '.z', '.Z')):
                files_to_process.append(os.path.join(extract_dir, extracted_file))


def process_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".crx"):
                crx_file = os.path.join(root, filename)
                rnx_file = crx_file.replace(".crx", ".rnx")
                print(f"Converting {crx_file} to {rnx_file}")
                # Пример команды для конвертации .crx в .rnx
                subprocess.run(["crx2rnx", crx_file, "-f"])
            elif filename.endswith(".24d"):
                d_file = os.path.join(root, filename)
                o_file = d_file.replace(".24d", ".24o")
                print(f"Converting {d_file} to {o_file}")
                # Пример команды для конвертации .24d в .24o
                subprocess.run(["crx2rnx", d_file, "-f"])


if __name__ == "__main__":
    # Находим последний загруженный zip-файл в директории 'downloads'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    archive_file = find_latest_zip(current_dir)

    if archive_file is None:
        print("В директории downloads не найдено zip-файлов.")
    else:
        extract_dir = 'extracted_data'

        # Распаковка вложенных сжатых файлов из найденного zip-файла
        extract_nested_files(archive_file, extract_dir)

        # Обработка файлов .crx и .24d в распакованной директории
        process_files(extract_dir)
