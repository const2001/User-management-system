# This is an official Python runtime, used as the parent image
FROM python:3.6.5-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory to the container as /app
ADD . /app

# Upgrade pip and install the required dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Unblock port 8000 for the Flask app to run on
EXPOSE 8001

# Execute the Flask app and the Kafka producer and consumer
CMD ["python", "app.py"]
