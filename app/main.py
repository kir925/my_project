from fastapi import FastAPI
import asyncio
from .publisher import start_publishing

app = FastAPI()

@app.post("/start/{satellite}")
async def start_satellite_data(satellite: str):
    # Здесь можно добавить логику для фильтрации по satellite
    asyncio.create_task(start_publishing(satellite))
    return {"message": f"Started publishing data for {satellite}"}

