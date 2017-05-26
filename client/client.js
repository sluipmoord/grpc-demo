const grpc = require('grpc');
const express = require('express');
const config = require('config');
const winston = require('winston');
const { isNumber, toNumber, isNaN } = require('lodash');

const grpcConfig = config.get('grpc');
const expressCongfig = config.get('express');
const { WeatherService } = grpc.load(grpcConfig.protoPath);

const client = new WeatherService(
  grpcConfig.address, grpc.credentials.createInsecure());

const app = express();

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

    client.getWeather({ id, name, code }, function (error, response) {
      if (error) {
        next(error);
      } else {
        res.json(response);
      }
    });

  } catch (error) {
    console.log('here');
    next(error);
  }
});

app.listen(expressCongfig['port'], function () {
  winston.info(
    'Example app listening on port %s!', config.get('express')['port'])
})
