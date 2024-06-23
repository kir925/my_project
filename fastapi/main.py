from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.post("/request-data/")
async def request_data(satellite_name: str):
    subprocess.Popen(["python", "/app/data_downloader/uploading_files.py", satellite_name])
    return {"message": "Processing started"}

