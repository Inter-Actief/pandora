# Production

## Prerequisites
Make sure Docker and Docker Compose are installed on your system.

## Setup
TODO

Run the following commands in the Docker container (`docker exec -it <container id> bash`).
```bash
# Seed database
poetry run python manage.py loaddata **/fixtures/*.json

# Create super user
poetry run python manage.py createsuperuser
```

TODO
