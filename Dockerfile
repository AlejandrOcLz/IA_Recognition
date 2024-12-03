FROM alpine:3.20
FROM python:3.8

WORKDIR /app

# Instalar las herramientas necesarias para compilar dlib y otras dependencias
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk2.0-dev \
    libboost-python-dev \
    python3-dev \
    && apt-get clean

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]