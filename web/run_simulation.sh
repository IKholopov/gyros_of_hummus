#!/bin/bash
SRV=localhost
while true
do
    curl "http://$SRV/iterate/"
    curl --data "user_id=1" http://$SRV/create_route/
    sleep 5
done
