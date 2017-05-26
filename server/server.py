import os
import grpc
import time
import pyowm

from concurrent import futures

import WeatherService_pb2
import WeatherService_pb2_grpc

OPEN_WEATHER_MAP_API_KEY = os.getenv(
    'WEATHER_API_KEY', 'bf660ad49156aaea0bcc911d701a456f')
TEMPERATURE_UNIT = os.getenv(
    'TEMPERATURE_UNIT', 'celsius')
SERVER_ADDRESS = os.getenv('SERVER_ADDRESS', '[::]:50051')

DAY_IN_SECONDS = 60 * 60 * 24

class WeatherService(WeatherService_pb2_grpc.WeatherServiceServicer):
    def __init__(self):
        self.api = pyowm.OWM(OPEN_WEATHER_MAP_API_KEY)

    def GetWeather(self, request, context):
        city_id = request.id
        city_name = request.name
        city_code = request.code

        observation = None

        print(city_id, city_name, city_code)
        if city_id:
            observation = self.api.weather_at_id(city_id)
        else:
            observation = self.api.weather_at_place(
                '{},{}'.format(city_name, city_code))

        weather = observation.get_weather()
        temperature = weather.get_temperature(TEMPERATURE_UNIT)
        return WeatherService_pb2.Weather(
            temp=temperature.get('temp', None),
            pressure=weather.get_pressure().get('press', None),
            humidity=weather.get_humidity(),
            temp_min=temperature.get('temp_min', None),
            temp_max=temperature.get('temp_max', None),
            unit=TEMPERATURE_UNIT
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    WeatherService_pb2_grpc.add_WeatherServiceServicer_to_server(
        WeatherService(), server)
    server.add_insecure_port(SERVER_ADDRESS)
    server.start()
    print('Server running on {}'.format(SERVER_ADDRESS))
    try:
        while True:
            time.sleep(DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
