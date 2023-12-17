FROM python:3.11-slim as base

WORKDIR /
RUN mkdir /logs

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Copy the requirements.txt file to the container
COPY ./requirements.txt /

# Install dependencies using pip
RUN pip3 install --no-cache-dir -r /requirements.txt

# Expose port for the application

### DEVELOPMENT ###
FROM base as development

# Copy your application code into the container
COPY . .

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8002", "--reload", "--reload-dir", "/app", "--access-log"]

### PRODUCTION ###
FROM base as production

# Copy your application code into the container
COPY . .

# Install production dependencies using pip
RUN pip3 install --no-cache-dir -r /requirements.txt

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001", "app.api:app"]
