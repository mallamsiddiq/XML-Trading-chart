#!/bin/bash

# Run commands inside the running "web" container

docker-compose run web python manage.py migrate
docker-compose run web python manage.py flush
docker-compose run web python manage.py makeadmin
docker-compose run web python manage.py seed_traders
docker-compose run web python manage.py simulate_profit_loss