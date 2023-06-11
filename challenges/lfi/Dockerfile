# Use the official PHP base image with version 7.4
FROM php:7.4-apache

COPY flag.txt /etc
# Set the working directory in the container
WORKDIR /var/www/html

# Copy the website files to the container
COPY app .


# Install dependencies, if any
# For example, if you have a composer.json file:
RUN apt update && apt install -y zip 
#     curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer && \
#     composer install --no-interaction --no-dev --prefer-dist

# Expose the port that Apache listens on
EXPOSE 80

# Start the Apache web server
CMD ["apache2-foreground"]
