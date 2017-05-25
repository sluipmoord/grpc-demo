python -m grpc_tools.protoc -I protos --python_out=/server/. --grpc_python_out=/server/. protos/WeatherService.proto
python server/server.py
