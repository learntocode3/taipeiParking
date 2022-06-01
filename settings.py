import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
RDS_HOST=os.getenv('RDS_HOST')
USER=os.getenv('Ezpark_USER')
PASSWORD=os.getenv('Ezpark_PASSWORD')
GOOGLE_API=os.getenv('googleApi')
PARTNER_KEY=os.getenv('PARTNER_KEY')
AWS_KEY_ID=os.getenv('AWS_KEY_ID')
AWS_SECRET_KEY=os.getenv('AWS_SECRET_KEY')
MIDDLEWARE_USERNAME=os.getenv('MIDDLEWARE_USERNAME')
MIDDLEWARE_PASSWORD=os.getenv('MIDDLEWARE_PASSWORD')
