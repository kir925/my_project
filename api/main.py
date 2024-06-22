from fastapi import FastAPI, BackgroundTasks
import subprocess

app = FastAPI()

def run_simulation(satellite: str):
    # Запускаем процесс симуляции в фоновом режиме
    subprocess.run(['python', 'simulate_and_publish.py', satellite])

@app.get("/simulate/{satellite}")
async def simulate_data(satellite: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_simulation, satellite)
    return {"message": f"Simulation started for satellite {satellite}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

