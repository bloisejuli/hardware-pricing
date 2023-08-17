#from sqlalchemy import create_engine as create_engine_alchemy

#def create_engine():
#    database_name = 'hardware_pricing'
#    username = 'root'
#    password = ''
#    host = 'localhost'
#    port = '3306'
#    engine = create_engine_alchemy(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}')
#    return engine

import mysql.connector
from sqlalchemy import create_engine as create_engine_alchemy

def create_connection():
    mydb = mysql.connector.connect(
        host = 'localhost',
        database_name = 'hardware_pricing',
        user = 'root',
        password = '',
        port = '3306'
    )
    return mydb, mydb.cursor(buffered=True)

def create_engine():
    database_name = 'hardware_pricing',
    username = 'root',
    password = '',
    host = 'localhost',
    port = '3306',
    engine = create_engine_alchemy(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}')
    return engine