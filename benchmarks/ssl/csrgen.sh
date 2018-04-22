#!/bin/sh

a=2
while [ "$a" -lt 21 ];    # this is loop1
do
	openssl req -new -key app$a.key -out app$a.csr
	a=$((a+1))

done
