# Use the official Python image as the parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the app files into the container at /app
COPY app .

# Install the required packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port 9000
EXPOSE 9000

# Define environment variables
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 9000

# Run the command to start the server
CMD ["flask", "run"]