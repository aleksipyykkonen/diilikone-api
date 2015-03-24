import os

SECRET_KEY = 'development_key'

DEBUG = True

MAIL_SERVER = os.environ.get(
    'MAIL_SERVER', 'smtp.mandrillapp.com')

MAIL_PORT = os.environ.get(
    'MAIL_PORT', 587)

MAIL_USERNAME = os.environ.get(
    'MAIL_USER')

MAIL_PASSWORD = os.environ.get(
    'MAIL_KEY')

MAIL_DEFAULT_SENDER = os.environ.get(
    'MAIL_SENDER', ('diili@apy.fi'))

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'postgres://localhost/diilikone'
)
CORS_HEADERS = 'Content-Type'
