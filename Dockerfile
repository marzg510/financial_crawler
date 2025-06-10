# Python image to use.
FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt --root-user-action=ignore --no-cache-dir

# Playwrightのブラウザバイナリをインストール
RUN playwright install --with-deps

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Run app.py when the container launches
# ENTRYPOINT ["python", "app.py"]
