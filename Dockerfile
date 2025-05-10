FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt