const grpc = require('grpc');
const { WeatherService } = grpc.load('../protos/WeatherService.proto');

const client = new WeatherService('localhost:50051', grpc.credentials.createInsecure())


client.getWeather({
  id: 1
}, function (error, response){
  console.log(response);
  console.error(error);
})
