from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import json

app = FastAPI()

def load_csv():
    try:
        df = pd.read_csv('data.csv')
        return df.to_dict('records')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []

data = load_csv()

@app.get("/", response_class=JSONResponse)
async def get_json():
    """
    Returns raw JSON data
    """
    return data

@app.get("/view", response_class=HTMLResponse)
async def view_json():
    """
    Returns HTML page with formatted JSON
    """
    html_content = f"""
    <html>
        <head>
            <title>CSV Data as JSON</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f0f0f0;
                }}
                pre {{
                    background-color: white;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    overflow-x: auto;
                }}
            </style>
        </head>
        <body>
            <h1>CSV Data as JSON</h1>
            <pre>{json.dumps(data, indent=2)}</pre>
        </body>
    </html>
    """
    return html_content

@app.get("/status")
async def status():
    return {
        "status": "online",
        "records_loaded": len(data),
        "endpoints": {
            "/": "Get raw JSON data",
            "/view": "View formatted JSON in browser",
            "/status": "API status"
        }
    }