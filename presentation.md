name: default
layout: true
class: center, middle
---
name: inverse
layout: true
class: center, middle, inverse
---
template: default
background-image: url(grpc_square_reverse_4x.png)
---
## A high performance, open-source universal RPC framework
---
layout: false
.left-column[
  ## What is it?
]
.right-column[
- In gRPC, a client application can directly call methods on a server application on a different machine as if it was a local object. This makes it easier for you to create distributed applications and services

- gRPC clients and servers can run and talk to each other in a variety of environments - from cloud server to your mobile device - and can be written in any of gRPC’s supported languages 10 to be precise (In the demo we are using python for the server and JavaScript for the client)

- By default gRPC uses protocol buffers, Google’s mature open source mechanism for serializing structured data and does support other data formats like JSON

- Netflix, Square, Docker and Cisco re some of the early adopters

- Visit [the website](http://www.grpc.io/docs/guides/index.html) for more detailed info
]
---
layout: false
.left-column[
  ## What is it?
  ## Benefits
]
.right-column[
- Simple service definition

- Works across languages and platforms

- Start quickly and scale

- Highly efficient on wire and with a simple service definition framework

- Start Bi-directional streaming and integrated auth

- Follows HTTP semantics over HTTP/2

- Developed with a microservice architecture in mind

- Pluggable auth, tracing, load balancing and health checking
]
---
layout: false
.left-column[
  ## What is it?
  ## Benefits
  ## Downside
]
.right-column[
- Poor browser support

- HTTP/2 Support is limited
]
---
template: inverse
## Proto Files (Protocol Buffers)
---
layout: false
.left-column[
  ## What is it?
]
.right-column[
- Protocol buffers are a flexible, efficient, automated mechanism for serializing structured data (Like XML, but smaller, faster, and simpler)

- You define how you want your data to be structured once, then you can use special generated source code to easily write and read your structured data to and from a variety of data streams and using a variety of languages.

- You can even update your data structure without breaking deployed programs that are compiled against the "old" format.

]
---
layout: false
.left-column[
  ## What is it?
  ## Example
]
.right-column[
```
syntax = "proto3";

service WeatherService {
  rpc GetWeather(City) returns (Weather) {};
}

message City {
  int32 id = 1;
  string name = 2;
  string code = 3;
}

message Weather {
  double temp = 1;
  double pressure = 2;
  double humidity = 3;
  double temp_min = 4;
  double temp_max = 5;
  string unit = 6;
}
```
]
---
template: inverse
## With our example proto file lets write a Pyhton Server implementation
---
layout: false
.left-column[
  ## STEP 1
]
.right-column[
### We need to setup our python environment

```
$ python -m pip install virtualenv
$ virtualenv env
$ source env/bin/activate
$ python -m pip install --upgrade pip
$ python -m pip install grpcio grpcio-tools
```
]
---
layout: false
.left-column[
  ## STEP 1
  ## STEP 2
]
.right-column[

### We need to compile our proto file

- The compiler generates the code in your chosen language you'll need to work with the message types you've described in the file, including getting and setting field values, serializing your messages to an output stream, and parsing your messages from an input stream.

```
$ python -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/WeatherService.proto
```
]
---
layout: false
.left-column[
  ## STEP 1
  ## STEP 2
  ## STEP 3
]
.right-column[
### Write our WeatherService stub server based on our proto

```
import WeatherService_pb2
import WeatherService_pb2_grpc


class WeatherService(WeatherService_pb2_grpc.WeatherServiceServicer):

    def GetWeather(self, request, context):
        city_id = request.id
        city_name = request.name
        city_code = request.code

        return WeatherService_pb2.Weather(
            temp=None,
            pressure=None,
            humidity=None,
            temp_min=None,
            temp_max=None,
            unit=None,
        )
```
]
---
layout: false
.left-column[
  ## STEP 1
  ## STEP 2
  ## STEP 3
  ## STEP 4
]
.right-column[
### Starting the server

```
DAY_IN_SECONDS = 60 * 60 * 24
SERVER_ADDRESS = os.getenv('SERVER_ADDRESS', '[::]:50051')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    WeatherService_pb2_grpc.add_WeatherServiceServicer_to_server(
        WeatherService(), server)
    server.add_insecure_port(SERVER_ADDRESS)
    server.start()
    print('Server running on {}'.format(SERVER_ADDRESS))

    # Because start() does not block you may need to
    # sleep-loop if there is nothing else for your code to do while serving.

    try:
        while True:
            time.sleep(DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
```
]
---
layout: false
.left-column[
  ## STEP 1
  ## STEP 2
  ## STEP 3
  ## STEP 4
  ## Finally
]
.right-column[
- Running the server

- ```
$ python server.py
```
- ```
$ Server running on [::]:50051
```
]
---
template: inverse
## Now let us write in a client in JavaScript (Everyone's favorite language) and expose a REST service
---
layout: false
.left-column[
  ## STEP 1
]
.right-column[
### Setting up the node environment

- Install node
```
$ curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash
```
- Install project dependencies
```
$ npm install
```
- Setup run scripts in package.json file
```
"scripts": {
    "start": "node client.js",
    "start:dev": "nodemon client.js"
}
```
]
---
layout: false
.left-column[
  ## STEP 1
  ## STEP 2
]
.right-column[
### Create our grpc client based on the proto file

```
const grpc = require('grpc');
const { WeatherService } = grpc.load("../protos/WeatherService.proto");
const client = new WeatherService(
  "localhost:50051", grpc.credentials.createInsecure());
```
### Create our http server

```
const express = require('express');

const app = express();

app.get('/weather', function (req, res, next) {
  res.status(501).send();
});

app.listen(3000, function () {
  winston.info('Example app listening on port %s!', 3000);
})
```
]
---
layout: false
.left-column[
  ## STEP 1
  ## STEP 2
  ## STEP 3
]
.right-column[
### Call our gRPC client
```
app.get('/weather', function (req, res, next) {
  try {
    const {
      'city-id': cityId,
      'city-name': name,
      'city-code': code
    } = req.query;

    let id;
    if (cityId !== undefined) {
      let id = toNumber(cityId);

      if (!isNumber(id) || isNaN(id)) {
        throw new Error(`city-id '${cityId}' is not a valid id`);
      }
    }
    // Calling the Weather Service
    client.getWeather({ id, name, code }, function (error, response) {
      if (error) {
        next(error);
      } else {
        res.json(response);
      }
    });

  } catch (error) {
    next(error);
  }
});
```
]
---
layout: false
.left-column[
  ## STEP 1
  ## STEP 2
  ## STEP 3
  ## STEP 4
]
.right-column[
### Running the GRPC client and web server
```
$ npm run start:dev

$ nodemon client.js
[nodemon] 1.11.0
[nodemon] to restart at any time, enter `rs`
[nodemon] watching: *.*
[nodemon] starting `node client.js`

info: Example app listening on port 3000!
```
]
---
template: inverse
## Lets integrate with a weather API and call our REST API
---
layout: false
.left-column[
  ## STEP 1
]
.right-column[
  ### Complete the server stub
  .small[

  ```
  import pyowm

  OPEN_WEATHER_MAP_API_KEY = os.getenv('WEATHER_API_KEY', 'bf660ad49156aaea0bcc911d701a456f')
  TEMPERATURE_UNIT = os.getenv('TEMPERATURE_UNIT', 'celsius')

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
  ```
  ]
]
---
layout: false
.left-column[
  ## STEP 1
  ## STEP 2
]
.right-column[
- Restart the server

- ```
$ python server.py
```
- ```
$ Server running on [::]:50051
```

- So now we can preform a GET on http://localhost:3000/weather?city-name=Pretoria

  ```
  {
    "temp":20.74,
    "pressure":1020,
    "humidity":35,
    "temp_min":19,
    "temp_max":22,
    "unit":"celsius"
  }
  ```
]
---
template: inverse

# *Commence exit dance*
<iframe src="https://giphy.com/embed/pa37AAGzKXoek" width="480" height="362" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/dancing-fresh-prince-of-bel-air-carlton-pa37AAGzKXoek">via GIPHY</a></p>
