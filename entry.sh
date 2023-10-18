#!/bin/bash

# Check if Docker is running

# Create a flag file to check if the initial setup has been completed
INITIAL_SETUP_FLAG_FILE=".initial_setup_completed"

# Check if the flag file exists
if [ ! -f "$INITIAL_SETUP_FLAG_FILE" ]; then
  echo "Initial setup has not been completed yet. Starting the setup..."

  # Build the Docker containers (if not already built)
  docker-compose build

  # Start the Docker containers in detached mode
  docker-compose up -d

  # Wait for the Django app to be ready (you can customize this part)
  until docker-compose exec web python -c "import requests; assert requests.get('http://web:8000/home').status_code == 200"
  do
    echo "Waiting for the Django app to start..."
    sleep 5
  done

  # Run initial setup tasks
  docker-compose exec web python manage.py migrate
  docker-compose exec web python manage.py makeadmin
  docker-compose exec web python manage.py seed_traders

  # Create the flag file to indicate that the initial setup is complete
  touch "$INITIAL_SETUP_FLAG_FILE"

  echo "Initial setup completed."

else
  # The initial setup has already been completed, so just start the containers
  docker-compose up -d

  echo "Django app is up and running at http://localhost:8000"
fi
