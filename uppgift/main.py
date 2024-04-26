import requests
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI()

security = HTTPBasic()

# Sätter inloggningsuppgifter
USERNAME = "admin"
PASSWORD = "admin"

WEATHER_API_URL = "http://api.weatherapi.com/v1"

WEATHER_API_KEY = "cc7abbeda00b4f34a4d61421242304"

# Funktion för att autentisera användare som jag sen sätter som dependency i mina endpoints
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == USERNAME and credentials.password == PASSWORD:
        return True
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

# Funktion för att hämta väderdata från WeatherAPI
def get_weather(city: Optional[str] = None, longitude: Optional[float] = None, latitude: Optional[float] = None):
    url = f"{WEATHER_API_URL}/current.json"
    params = {"key": WEATHER_API_KEY}

    if city:
        params["q"] = city
    elif longitude is not None and latitude is not None:
        params["q"] = f"{longitude},{latitude}"
    else:
        raise ValueError("Either city name or longitude/latitude must be provided.")

    response = requests.get(url, params=params)
    return response.json()

# Endpoints för att hämta väderdata antingen via stad eller koordinater
@app.get("/weather/{city}")
def weather_data_city(city: str, credentials: HTTPBasicCredentials = Depends(authenticate)):
    weather_data = get_weather(city)
    return weather_data


@app.get("/weather/{longitude}/{latitude}")
def weather_data_coordinates(longitude: float, latitude: float, credentials: HTTPBasicCredentials = Depends(authenticate)):
    weather_data = get_weather(longitude=longitude, latitude=latitude)
    return weather_data

# Data för sensorer
temp_sensor_id = [20, 19.5]
rad_sensor_id = [True, True, False, False]
curtain_sensor_id = [True, False, True, False, True]

# Funktioner för att läsa data från sensorer
def read_temperature(sensor_id: int):
    temperature = temp_sensor_id[sensor_id]
    return temperature

def read_radiator(radiator_id: int):
    radiator_status = rad_sensor_id[radiator_id]
    return radiator_status

def read_curtains(curtain_id: int):
    curtains_status = curtain_sensor_id[curtain_id]
    return curtains_status

# Funktion för att räkna ut medeltemperaturen och kollar om det finns någon data för att inte dela med 0
def read_avg_temperature(sensor_data: list):
    if not sensor_data:
        return None  

    avg_temperature = sum(sensor_data) / len(sensor_data)
    return avg_temperature



# Klasser som visar vad för data som ska skickas till API:et
class TemperatureUpdate(BaseModel):
    temperature: float

class RadiatorUpdate(BaseModel):
    status: bool

class CurtainUpdate(BaseModel):
    status: bool

# Get metoder för att hämta data från sensorer
@app.get("/temperature/{sensor_id}")
def get_temperature(sensor_id: int, credentials: HTTPBasicCredentials = Depends(authenticate)):
    temperature = read_temperature(sensor_id)
    return {"sensor_id": sensor_id, "temperature": temperature}

@app.get("/avg_temperature")
def get_avg_temperature():
    avg_temperature = read_avg_temperature(sensor_data=temp_sensor_id)
    return {"avg_temperature": avg_temperature}

@app.get("/radiator/{radiator_id}")
def get_radiator(radiator_id: int, credentials: HTTPBasicCredentials = Depends(authenticate)):
    radiator_status = read_radiator(radiator_id)
    return {"radiator_id": radiator_id, "status": radiator_status}

@app.get("/curtains/{curtain_id}")
def get_curtains(curtain_id: int, credentials: HTTPBasicCredentials = Depends(authenticate)):
    curtain_status = read_curtains(curtain_id)
    return {"curtain_id": curtain_id, "status": curtain_status}

# Post metoder för att ändra "sensorer"
@app.post("/radiator/{radiator_id}")
def turn_on_radiator(radiator_id: int, radiator_update: RadiatorUpdate, credentials: HTTPBasicCredentials = Depends(authenticate)):
    rad_sensor_id[radiator_id] = radiator_update.status
    return {"message": f"Radiator status updated for radiator {radiator_id} to {radiator_update.status}"}

@app.post("/curtains/{curtain_id}")
def roll_up_curtains(curtain_id: int, curtain_update: CurtainUpdate, credentials: HTTPBasicCredentials = Depends(authenticate)):
    return {"message": f"Curtains status updated for curtain {curtain_id} to {curtain_update.status}"}

@app.post("/change_temperature")
def change_temperature(temperature_update: TemperatureUpdate, credentials: HTTPBasicCredentials = Depends(authenticate)):
    return {"message": f"Temperature updated to {temperature_update.temperature}"}
