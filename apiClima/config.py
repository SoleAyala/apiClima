import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/api_clima')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


