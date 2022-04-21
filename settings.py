import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
# USER=os.getenv('USER_TAIPEI')
# PASSWORD=os.getenv('PASSWORD')
# PARTNER_KEY=os.getenv('PARTNER_KEY')
