from sqlalchemy import create_engine

def create_engine_mysql():
    database_name = 'hardware_pricing'
    username = 'root'
    password = 'oycobe'
    host = 'localhost'
    port = 3306
    engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}')
    return engine