#!/bin/bash
echo 'run after_install.sh: ' >> /home/ec2-user/solar-wind-api/deploy.log

echo 'cd /home/ec2-user/solar-wind-api' >> /home/ec2-user/solar-wind-api/deploy.log
cd /home/ec2-user/solar-wind-api >> /home/ec2-user/solar-wind-api/deploy.log

echo 'source bin/activate' >> /home/ec2-user/solar-wind-api/deploy.log 
source bin/activate >> /home/ec2-user/solar-wind-api/deploy.log

echo 'pip install -r requirements.txt' >> /home/ec2-user/solar-wind-api/deploy.log 
source pip install -r requirements.txt >> /home/ec2-user/solar-wind-api/deploy.log

echo 'alembic upgrade head' >> /home/ec2-user/solar-wind-api/deploy.log
alembic upgrade head >> /home/ec2-user/solar-wind-api/deploy.log