from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import pytz
from Moon_Calculations  import get_moon_parameters,calculate_q_and_visibility, get_sunset_time
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse,PlainTextResponse
import os
from typing import Optional

app = FastAPI()

# Serve index.html at the root URL
@app.get("/")
async def read_index():
    return FileResponse("index.html")
# app.mount("/static", StaticFiles(directory="."), name="static")


class MoonRequest(BaseModel):
    lat: float
    lon: float
    elevation: float = 0.0
    date: str  # Expected format "dd-mm-yyyy"
    timezone: str
    city: Optional[str] = None

@app.post("/moon_data")
def moon_data(request: MoonRequest):
    # Parse date string to datetime
    try:
        obs_date = datetime.strptime(request.date, "%d-%m-%Y")
    except ValueError:
        return {"error": "Date format should be dd-mm-yyyy"}

    # Apply timezone
    try:
        tz = pytz.timezone(request.timezone)
    except Exception:
        return {"error": "Invalid timezone"}

    obs_date = tz.localize(obs_date)

    # Calculate sunset datetime
    sunset_dt = get_sunset_time(request.lat, request.lon, obs_date, request.elevation)
        
    # Use sunset time to get moon parameters
    moon_params = get_moon_parameters(sunset_dt, request.lat, request.lon, request.elevation,request.city)


    return moon_params

