#!/bin/bash

ROOT_DIRECTORY=$(dirname "$(dirname "$0")")

poetry run python manage.py graph_models -a -X BaseModel -o "$ROOT_DIRECTORY/docs/diagrams/database.dot"
poetry run python manage.py graph_models -a -X BaseModel -o "$ROOT_DIRECTORY/docs/diagrams/database.png"
