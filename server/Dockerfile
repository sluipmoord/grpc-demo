FROM python:3.6-slim

RUN apt-get update && apt-get install python-dev python3-dev -y

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 50051

ENTRYPOINT ["python", "server.py"]
