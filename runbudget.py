# app.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

app = FastAPI()

# Load data from JSON instead of CSV to avoid numpy dependency
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

data = load_data()

@app.get("/")
async def read_root():
    return {"status": "API is running"}

@app.get("/data")
async def get_data():
    return JSONResponse(content=data)

@app.get("/status")
async def get_status():
    return {
        "status": "online",
        "records": len(data)
    }