import os
""" 
General settings for the project

"""
PRIVATE_KEY_PATH = os.path.expanduser('~/work/sidies/crossover/project/hawkeye/private_key')

DB_CREDENTIALS = {
    'host': '127.0.0.1',
    'port': 5432,
    'username': 'postgres',
    'password': 'postgres'
}

SMTP_SERVER_SETTINGS = {
    'host': 'smtp.gmail.com',
    'port': 587,
    'username': 'hisham.elsheshtawy@gmail.com',
    'password': 'Icandoitbefore25'
}

SMTP_SENDER_EMAIL = 'hisham.elsheshtawy@gmail.com'
