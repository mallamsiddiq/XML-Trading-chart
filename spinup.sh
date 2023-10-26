#!/bin/bash

# Run commands inside the running "web" container
docker exec -it web python manage.py flush
docker exec -it web python manage.py makeadmin
docker exec -it web python manage.py seed_traders
docker exec -it web python manage.py simulate_profit_loss


python manage.py migrate
python manage.py makeadmin
python manage.py seed_traders
python manage.py simulate_profit_loss