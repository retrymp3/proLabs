# Use the official Ubuntu image as the base image
FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive
# Update the package lists and install Apache and PHP
RUN apt-get update && \
    apt-get install -y apache2 php
# Set the working directory in the container
WORKDIR /var/www/html

# Copy the necessary files to the container
COPY index.html info.php login.php log.txt /var/www/html/
COPY style.css /var/www/html/

# Set permissions for the files
# RUN chown -R www-data:www-data /var/www/html \
#     && chmod -R 755 /var/www/html

# Enable Apache rewrite module for clean URLs
#RUN a2enmod rewrite

# Expose port 80 for web traffic
EXPOSE 80

# Start the Apache server
CMD ["apache2ctl", "-D", "FOREGROUND"]
