from fastapi import FastAPI, HTTPException
from pathlib import Path
from .download import download_file
from .process import convert_crx_to_rnx, decompress_files
from .mqtt_publisher import start_publisher

app = FastAPI()

DATA_DIR = Path("./data")

@app.get("/download")
def download_data(satellite: str, date: str):
    DATA_DIR.mkdir(exist_ok=True)
    
    data_dir = download_file(date, DATA_DIR)
    decompress_files(data_dir)
    convert_crx_to_rnx(data_dir)
    
    target_file = None
    for file in data_dir.glob(f"{satellite}_*.rnx"):
        target_file = file
        break

    if target_file is None:
        raise HTTPException(status_code=404, detail="Satellite data not found")

    start_publisher(target_file, satellite)

    return {"message": "Data is being published", "file": str(target_file)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

