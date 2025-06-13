FROM python:3.12-slim


RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    iproute2 \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Disable writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Define stdout/stderr as unbuffered
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/front/dit-app

COPY ./dit-app/requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY ./dit-app .

CMD ["tail", "-f", "/dev/null"]
# Start Streamlit server
# CMD ["streamlit", "run", "main.py"]
