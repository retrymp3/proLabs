FROM ubuntu:20.04
RUN apt update -yqq
RUN apt install curl -yqq
RUN curl -fsSL https://deb.nodesource.com/setup_16.x |  bash -
RUN apt-get install nodejs -yqq

WORKDIR /app
COPY src/package.json .
RUN npm install
COPY src .
COPY flag.txt /

CMD ["node","app.js"]