FROM ruby:2.7

WORKDIR /app

COPY app /app/

RUN apt-get update && apt-get install -y \
    ruby-full \
    ruby-dev \
    build-essential \
    libffi-dev \
    netcat \
    net-tools

RUN gem install sinatra

EXPOSE 4567

CMD ["ruby", "app.rb", "-o", "0.0.0.0"]
