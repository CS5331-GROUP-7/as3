#!/bin/sh
sudo cp -Rvf sites-enabled /etc/apache2/sites-enabled
cp -Rvf ssl /home/cs5331/Desktop
sudo cp -Rvf www /var/
sudo cp hosts /etc/hosts
sudo a2enmod ssl
sudo service apache2 restart

