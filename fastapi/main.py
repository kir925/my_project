# fastapi/main.py
from fastapi import FastAPI, HTTPException, Query
from pathlib import Path
from typing import Optional
from gnss_tec import rnx

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to GNSS Data Downloader"}

@app.post("/request-data/")
def request_data(date: str = Query(..., description="Date in YYYY-MM-DD format"),
                 satellite_name: str = Query(..., description="Name of the satellite")):
    directory_path = f"data_downloader/{date}/{satellite_name}"
    file_name = f"{satellite_name}_R_{date}_01D_30S_MO.rnx"
    file_path = Path(directory_path) / file_name

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File {file_name} not found for {satellite_name} on {date}")

    with open(file_path, 'r') as obs_file:
        reader = rnx(obs_file)
        tec_data = []
        for tec in reader:
            tec_data.append({
                "timestamp": tec.timestamp,
                "satellite": tec.satellite,
                "phase_tec": tec.phase_tec,
                "p_range_tec": tec.p_range_tec,
            })

    return {"date": date, "satellite_name": satellite_name, "tec_data": tec_data}
