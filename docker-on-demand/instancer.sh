#!/bin/bash
cd /home/chry5a0r/Desktop/Project/websec-pro-labs/docker-on-demand/instancer
python3 /home/chry5a0r/Desktop/Project/websec-pro-labs/docker-on-demand/instancer/app.py > log.txt 2>&1 &
echo "Frontend spawned"
cd /home/chry5a0r/Desktop/Project/websec-pro-labs/docker-on-demand/docker-on-demand/server
python3 /home/chry5a0r/Desktop/Project/websec-pro-labs/docker-on-demand/docker-on-demand/server/app.py > log.txt  2>&1 &
echo "Backend spawned"
#a