# app.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize empty data
data = []

# Safe data loading function
def load_data():
    global data
    try:
        # Print current directory and files for debugging
        print("Current directory:", os.getcwd())
        print("Files in directory:", os.listdir())
        
        # Load CSV with explicit encoding
        df = pd.read_csv('data.csv', encoding='utf-8')
        data = df.to_dict('records')
        print("Data loaded successfully")
        return True
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    load_data()

@app.get("/")
async def read_root():
    return {"status": "API is running"}

@app.get("/data")
async def get_data():
    if not data:
        return JSONResponse(
            content={"error": "No data available"},
            status_code=404
        )
    return JSONResponse(content=data)

@app.get("/status")
async def get_status():
    return {
        "status": "online",
        "data_loaded": bool(data),
        "record_count": len(data)
    }