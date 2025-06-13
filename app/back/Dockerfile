FROM python:3.12-slim

RUN apt-get update && \
    # -y: Automatically answers "yes" to prompts during the installation process
    apt-get upgrade -y && \
    # --no-install-recommends: install only the specified package and its essential dependencies, excluding any recommended (optional) packages
    apt-get install -y --no-install-recommends \
    iproute2 \
    curl \
    # For Postgres
    gcc \
    libpq-dev \
    # For PostGIS
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev && \
    # Removes cached files from /var/cache/apt/archives and /var/cache/apt/archives/partial that are used during the package installation process
    apt-get clean && \
    # Deletes the local copy of package metadata downloaded when you run apt-get update
    rm -rf /var/lib/apt/lists/*

# Disable writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Define stdout/stderr as unbuffered
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/back/dit-app

COPY ./dit-app/requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY ./dit-app .

# Keep container open for development
CMD ["tail", "-f", "/dev/null"]
# Start Django server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]