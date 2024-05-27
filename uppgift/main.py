from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import requests
from typing import Optional
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

security = HTTPBasic()

# Set credentials
USERNAME = "admin"
PASSWORD = "admin"

WEATHER_API_URL = "http://api.weatherapi.com/v1"
WEATHER_API_KEY = "cc7abbeda00b4f34a4d61421242304"

# Authenticate user function
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == USERNAME and credentials.password == PASSWORD:
        return True
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

# Function to get weather data from WeatherAPI
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

# Selenium function to fetch page title
def fetch_page_title(url: str) -> str:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    try:
        driver.get(url)
        title = driver.title
    finally:
        driver.quit()
    
    return title

# Endpoint to fetch weather data by city
@app.get("/weather/{city}")
def weather_data_city(city: str, credentials: HTTPBasicCredentials = Depends(authenticate)):
    weather_data = get_weather(city)
    return weather_data

# Endpoint to fetch weather data by coordinates
@app.get("/weather/{longitude}/{latitude}")
def weather_data_coordinates(longitude: float, latitude: float, credentials: HTTPBasicCredentials = Depends(authenticate)):
    weather_data = get_weather(longitude=longitude, latitude=latitude)
    return weather_data

# Endpoint to fetch page title using Selenium
@app.get("/fetch-title")
def fetch_title(url: str, credentials: HTTPBasicCredentials = Depends(authenticate)):
    title = fetch_page_title(url)
    return {"url": url, "title": title}

# Data for sensors
temp_sensor_id = [20, 19.5]
rad_sensor_id = [True, True, False, False]
curtain_sensor_id = [True, False, True, False, True]

# Functions to read sensor data
def read_temperature(sensor_id: int):
    temperature = temp_sensor_id[sensor_id]
    return temperature

def read_radiator(radiator_id: int):
    radiator_status = rad_sensor_id[radiator_id]
    return radiator_status

def read_curtains(curtain_id: int):
    curtains_status = curtain_sensor_id[curtain_id]
    return curtains_status

# Function to calculate average temperature
def read_avg_temperature(sensor_data: list):
    if not sensor_data:
        return None  
    avg_temperature = sum(sensor_data) / len(sensor_data)
    return avg_temperature

# Pydantic models for updating sensor data
class TemperatureUpdate(BaseModel):
    temperature: float

class RadiatorUpdate(BaseModel):
    status: bool

class CurtainUpdate(BaseModel):
    status: bool

# Endpoints to get sensor data
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

# Endpoints to update sensor data
@app.post("/radiator/{radiator_id}")
def turn_on_radiator(radiator_id: int, radiator_update: RadiatorUpdate, credentials: HTTPBasicCredentials = Depends(authenticate)):
    rad_sensor_id[radiator_id] = radiator_update.status
    return {"message": f"Radiator status updated for radiator {radiator_id} to {radiator_update.status}"}

@app.post("/curtains/{curtain_id}")
def roll_up_curtains(curtain_id: int, curtain_update: CurtainUpdate, credentials: HTTPBasicCredentials = Depends(authenticate)):
    curtain_sensor_id[curtain_id] = curtain_update.status
    return {"message": f"Curtains status updated for curtain {curtain_id} to {curtain_update.status}"}

@app.post("/change_temperature")
def change_temperature(temperature_update: TemperatureUpdate, credentials: HTTPBasicCredentials = Depends(authenticate)):
    global temp_sensor_id
    temp_sensor_id = [temperature_update.temperature] * len(temp_sensor_id)
    return {"message": f"Temperature updated to {temperature_update.temperature}"}
