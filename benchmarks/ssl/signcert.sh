#!/bin/sh

a=2
while [ "$a" -lt 21 ];    # this is loop1
do
	openssl ca -in app$a.csr -config openssl.cnf 
	a=$((a+1))
done
