#!/bin/bash

echo 'run application_start.sh: ' >> /home/ec2-user/solar-wind-api/deploy.log

echo 'sudo systemctl restart gunicorn' >> /home/ec2-user/solar-wind-api/deploy.log
sudo systemctl restart gunicorn >> /home/ec2-user/solar-wind-api/deploy.log