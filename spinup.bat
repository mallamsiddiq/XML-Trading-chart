echo Spinning up and seeding the database

:: Use the following commands to run Docker Compose commands with the correct service name "web"
docker-compose exec web python manage.py flush
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py makeadmin
docker-compose exec web python manage.py seed_traders
docker-compose exec web python manage.py simulate_profit_loss
