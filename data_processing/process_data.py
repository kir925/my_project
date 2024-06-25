import os
import subprocess

def process_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".crx"):
            crx_file = os.path.join(directory, filename)
            rnx_file = crx_file.replace(".crx", ".rnx")
            subprocess.run(["crx2rnx", crx_file, rnx_file])

if __name__ == "__main__":
    process_files('/path/to/unzipped/files')

