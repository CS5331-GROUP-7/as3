#!/bin/sh

a=2
while [ "$a" -lt 21 ];    # this is loop1
do
	openssl rsa -in app$a.key -out app$a-insecure.key
	a=$((a+1))
done
