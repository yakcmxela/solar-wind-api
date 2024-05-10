from ambient_api.ambientapi import AmbientAPI
from requests import get


class WeatherAPI:
    def __init__(self):
        self.api = AmbientAPI()

    async def get_weather_by_coords(self, lat: str, lng: str):
        public_url = "https://lightning.ambientweather.net/devices"
        nearest_station_response = get(
            f"{public_url}?$publicNear[coords][0]={lng}&$publicNear[coords][1]={lat}&$limit=1"
        )
        nearest_station_data = nearest_station_response.json()
        last_data = nearest_station_data["data"][0]["lastData"]

        solar_radiation = (
            last_data["hl"]["solarradiation"]["h"]
            + last_data["hl"]["solarradiation"]["l"]
        ) / 2
        wind_speed = (
            last_data["hl"]["windspeedmph"]["h"]
            + last_data["hl"]["windspeedmph"]["l"]
        ) / 2
        return {
            "solar_radiation": solar_radiation,
            "wind_speed": wind_speed,
        }
    
    async def get_weather_by_station():
        # Todo
        # self.api.get_weather()
        pass
