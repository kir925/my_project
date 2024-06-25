from fastapi import FastAPI, Query
from rinex_reader.rinex_reader import read_rinex_file
from typing import List

app = FastAPI()

@app.get("/subscribe/")
async def subscribe(satellite_name: List[str] = Query(None)):
    for sat_name in satellite_name:
        filename = f"{sat_name}_R_20240010000_01D_30S_MO.rnx"
        for data in read_rinex_file(f"rinex_reader/rinex_files/{filename}"):
            yield data

