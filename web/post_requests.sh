#!/bin/bash
SRV=localhost

while true
do
	curl "http://$SRV/navigate/?floor_from=0&x_from=15.417994&y_from=60.483762&floor_to=1&x_to=15.418110&y_to=60.485317&user_id=1"
	curl http://$SRV/create_route/ --data "user_id=1"
	sleep 10
	curl "http://$SRV/navigate/?floor_from=1&x_from=15.418270&y_from=60.484330&floor_to=0&x_to=15.418503&y_to=60.484684&user_id=3"
	curl http://$SRV/create_route/ --data "user_id=3"
	sleep 10
    curl "http://$SRV/navigate/?floor_from=2&x_from=15.418278&y_from=60.484265&floor_to=1&x_to=15.417881&y_to=60.484202&user_id=4"
    curl http://$SRV/create_route/ --data "user_id=4"
    curl "http://$SRV/navigate/?floor_from=2&x_from=15.417895&y_from=60.483546&floor_to=1&x_to=15.418110&y_to=60.485317&user_id=2"
    curl http://$SRV/create_route/ --data "user_id=2"
    sleep 10
done
