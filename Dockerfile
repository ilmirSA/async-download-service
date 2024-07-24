FROM python:3.10

RUN apt-get update && apt-get install -y zip

WORKDIR /app



COPY . .

RUN pip install -r requirements.txt

