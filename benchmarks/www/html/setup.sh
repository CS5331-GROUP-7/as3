#!/bin/bash

sudo apt-get update

sudo apt-get -y install libapache2-mod-php apache2
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password toor'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password toor'

sudo apt-get -y install mysql-server php-mysqli
echo "drop database sqli; drop database csrf;" | mysql -u root --password=toor
echo "create database sqli; create database csrf;" | mysql -u root --password=toor
echo "use sqli; create table users (username varchar(255), age int, school varchar(255));" | mysql -u root --password=toor
echo "use sqli; insert into users values ('Cat', 14, 'Hollywood High')" | mysql -u root --password=toor
echo "use sqli; insert into users values ('Tori', 15, 'Hollywood High')" | mysql -u root --password=toor
echo "use sqli; insert into users values ('Andre', 14, 'Hollywood High')" | mysql -u root --password=toor
echo "use sqli; insert into users values ('Robbie', 15, 'Hollywood High')" | mysql -u root --password=toor
echo "use sqli; insert into users values ('Beck', 16, 'Hollywood High')" | mysql -u root --password=toor
echo "use sqli; insert into users values ('Jade', 16, 'Hollywood High')" | mysql -u root --password=toor
echo "use sqli; insert into users values ('Harry', 12, 'Hogwarts')" | mysql -u root --password=toor
echo "use csrf; create table sensitives (indexno int, message varchar(255));" | mysql -u root --password=toor
echo "use csrf; insert into sensitives values (1, 'SECRET')" | mysql -u root --password=toor

sudo sh -c 'echo "127.0.0.1	target.com" >> /etc/hosts'

sudo cp -R * /var/www/html/

sudo service apache2 restart
