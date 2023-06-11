FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /src

# Copy the app files into the container at /app
COPY src .
# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 9000
EXPOSE 3000

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 3000

# Run the command to start the server
CMD ["flask", "run"]