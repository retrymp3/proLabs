FROM ubuntu:latest

WORKDIR /app
COPY ./src/requirements.txt /app
RUN apt update -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install -r requirements.txt
COPY ./src /app

CMD ["python3", "app.py"]