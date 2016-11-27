#!/bin/bash
SRV=localhost
while true
do
	curl "http://$SRV/iterate/"
	sleep 5
done
