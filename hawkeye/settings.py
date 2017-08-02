"""General settings for the project."""

import os

PRIVATE_KEY_PATH = os.path.expanduser('~/work/sidies/crossover/project/hawkeye/private_key')

DB_CREDENTIALS = {
    'host': os.environ.get('HAWKEYE_DB_HOST', '127.0.0.1'),
    'port': os.environ.get('HAWKEYE_DB_PORT', 5432),
    'username': os.environ.get('HAWKEYE_DB_USERNAME', 'postgres'),
    'password': os.environ.get('HAWKEYE_DB_PASSWORD', 'postgres'),
}

SMTP_SERVER_SETTINGS = {
    'host': os.environ.get('HAWKEYE_SMTP_HOST'),
    'port': os.environ.get('HAWKEYE_SMTP_PORT', 587),
    'username': os.environ.get('HAWKEYE_SMTP_USERNAME'),
    'password': os.environ.get('HAWKEYE_SMTP_PASSWORD')
}

SMTP_SENDER_EMAIL = os.environ.get('HAWKEYE_SENDER_EMAIL')
