import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
USER=os.getenv('Ezpark_USER')
PASSWORD=os.getenv('Ezpark_PASSWORD')
# PARTNER_KEY=os.getenv('PARTNER_KEY')
