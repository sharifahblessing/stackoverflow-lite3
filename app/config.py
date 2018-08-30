import psycopg2
import sys
import os
import datetime
import jwt
from datetime import datetime, timedelta
from flask import current_app



def configconnection():
    
    conn = psycopg2.connect(
            database="stackoverflow_db", user="postgres",  password="1234",host="localhost", port="5432"
        )
    
    return conn
def generate_token(username):
    """Generates the access token to be used as the Authorization header"""

    try:
        # set up a payload with an expiration time
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=30),
            # international atomic time
            'iat': datetime.utcnow(),
            # default  to user id
            'username': username
        }
        # create the byte string token using the payload and the SECRET key

        jwt_string = jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        ).decode('UTF-8')
        return jwt_string

    except Exception as e:
        # return an error in string format if an exception occurs
        return str(e)


def decode_token(token):
    """Decode the access token to get the payload 
    and return user_id and  field results"""
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        return {"username": payload['username'],
                "status": "Success"}
    except jwt.ExpiredSignatureError:
        return {"status": "Failure",
                "message": "Expired token. Please log in to get a new token"}
    except jwt.InvalidTokenError:
        return {"status": "Failure",
                "message": "Invalid token. Please register or login"}



class BaseConfig(object):
    """
    Common configurations
    """
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    # Put any configurations here that are common across all environments


class TestingConfig(BaseConfig):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    """
    Development configurations
    """

    DEBUG = True


class ProductionConfig(BaseConfig):
    """
    Production configurations
    """

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}