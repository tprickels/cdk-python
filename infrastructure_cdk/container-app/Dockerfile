FROM ubuntu

ENV TZ=Etc/UTC
ENV DEBIAN_FRONTEND=noninteractive

# Install apache and remove the downloaded packages
RUN apt-get update -y && apt-get install -y apache2 && rm -r /var/lib/apt/lists/*

COPY webapp /var/www/html

EXPOSE 80
