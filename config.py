import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class  Config(object):
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SALT_KEY="QAZWSX"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    APP_SECRET = os.environ.get('APP_SECRET')