import os

# from dotenv import load_dotenv

# load_dotenv('../../../.env')

BACKEND_HOST = os.getenv('BACKEND_HOST')
BACKEND_PORT = os.getenv('BACKEND_PORT')

BACKEND_HOST = 'srv-dit-back'
BACKEND_PORT = 8000
# BACKEND_PORT = 8100
BACKEND_URL = f'http://{BACKEND_HOST}:{BACKEND_PORT}'

GENERIC_REQUEST_ERROR = 'Service error'