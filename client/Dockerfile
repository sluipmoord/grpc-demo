FROM node:6-slim

WORKDIR /app

COPY . /app

RUN npm install

EXPOSE 3000

ENTRYPOINT ["node", "client.js"]
