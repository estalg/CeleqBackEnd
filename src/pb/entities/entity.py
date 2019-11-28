from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = '10.90.85.68'
db_name = 'celeq_data_base'
db_user = 'admin'
db_password = 'Adminsql$celeq'

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()