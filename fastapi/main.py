from fastapi import FastAPI, HTTPException
import subprocess
import os
import sys

app = FastAPI()

@app.post("/request-data/")
async def request_data(satellite_name: str):
    script_path = "/app/data_downloader/uploading_files.py"
    result = subprocess.run(["python3", script_path, satellite_name], capture_output=True, text=True)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr)
    return {"message": result.stdout}
