# grpc-demo.io
Demo using open weather api to write a GRPC Server and Client

## Server
  - cd server
  - virtualenv -p python3 env
  - . env/bin/activate
  - pip install -r requirements.txt
  - ./run_server

## Client
  - cd client
  - yarn install / npm install
  - yarn start / npm start


Example GET request:
`http://localhost:3000/weather?city-name=Pretoria,city-code=za`
Response:
```
{
  "temp": 18.97,
  "pressure": 1021,
  "humidity": 28,
  "temp_min": 17,
  "temp_max": 21,
  "unit": "celsius"
}
```
