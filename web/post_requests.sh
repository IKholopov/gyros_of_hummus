#!/bin/bash
SRV=localhost

#    while true
 #   do
	curl "http://$SRV/navigate/?floor_from=0&x_from=15.417994&y_from=60.483762&floor_to=1&x_to=15.418110&y_to=60.485317&user_id=1"
	curl http://$SRV/create_route/ --data "user_id=1"
	sleep 20
#	curl http://$(SRV)/navigate/?floor_from=1&x_from=15.417895&y_from=60.483546&floor_to=0&x_to=15.418110&y_to=60.485317&user_id=1
 #       curl http://$(SRV)/create_route --data "user_id=1"
  #      sleep 20
#    done
