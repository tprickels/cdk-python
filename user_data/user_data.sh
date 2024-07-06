#!/bin/bash

apt-get update -y
apt-get install -y apache2

echo "Welcome Home" >> /var/www/html/index.html

systemctl enable apache2 --now
