# Use Python as base image
FROM python:latest

# Install dependencies
RUN apt update && apt install -y build-essential default-libmysqlclient-dev gdal-bin gettext libgraphviz-dev libproj-dev redis

# Install Poetry
RUN pip install poetry

# Create user
RUN useradd -m worker

# Create working directory
RUN mkdir -p /srv/app && chown -R worker:worker /srv/app
WORKDIR /srv/app
USER worker

# Copy pyproject.toml and poetry.lock so Docker can cache dependencies
COPY --chown=worker:worker pyproject.toml /srv/app
COPY --chown=worker:worker poetry.lock /srv/app

# Install app dependencies
RUN poetry install

# Copy app source
COPY --chown=worker:worker . /srv/app
RUN touch .production && mkdir -p /srv/app/dist/static

# Expose default port
EXPOSE 3000

# Define entrypoint and command of the app
ENTRYPOINT ["/bin/sh"]
CMD ["/srv/app/scripts/start_server.sh"]
