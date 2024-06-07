from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine 
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_USER


URL_DATABASE = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
