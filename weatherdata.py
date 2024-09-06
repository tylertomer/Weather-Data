import requests
import pandas as pd

API_KEY = "Key goes here"
LATITUDE = 37.0025
LONGITUDE = -86.3716639

AREA = 4 
EFFICIENCY = 0.23

URL = f'https://api.solcast.com.au/data/live/radiation_and_weather?latitude={LATITUDE}&longitude={LONGITUDE}&output_parameters=air_temp,dni,ghi,albedo,azimuth,clearsky_dhi,clearsky_dni,clearsky_ghi,clearsky_gti,cloud_opacity,cloud_opacity10,cloud_opacity90,dewpoint_temp,dhi,dhi10,dhi90,dni10,dni90,ghi10,ghi90,gti,gti10,gti90,precipitable_water,precipitation_rate,relative_humidity,surface_pressure,snow_depth,snow_soiling_rooftop,snow_soiling_ground,snow_water_equivalent,wind_direction_100m,wind_direction_10m,wind_speed_100m,wind_speed_10m,zenith&format=json&api_key={API_KEY}'

def fetch_weather_data():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        measurements = data.get('measurements', [])
        return pd.DataFrame(measurements)
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def process_weather_data(weather_data):
    if weather_data is not None:
        weather_data['period_end'] = pd.to_datetime(weather_data['period_end'])
        weather_data.set_index('period_end', inplace=True)
        filtered_data = weather_data.between_time('09:00', '18:00')
        return weather_data
    else:
        return None

def estimate_power_generation(filtered_data):
    if filtered_data is not None:
        filtered_data['estimated_power_kw'] = filtered_data['ghi'] * AREA * EFFICIENCY / 1000
        total_power_generated = filtered_data['estimated_power_kw'].sum()
        print(f"Total estimated power generation: {total_power_generated:.2f} kWh")
    else:
        print("No data")

def display_forecast(processed_data):
    if processed_data is not None:
        print("Weather Forecast for Solar Car Race:")
        print(processed_data.head(10))
    else:
        print("No data")

if __name__ == "__main__":
    weather_data = fetch_weather_data()
    processed_data = process_weather_data(weather_data)
    display_forecast(processed_data)
    estimate_power_generation(processed_data)
