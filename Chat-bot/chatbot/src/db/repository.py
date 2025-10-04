from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.model.models import Base

class Database:
    def __init__(self, db_config):
        self.engine = create_engine(db_config['DATABASE_URL'])
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self):
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()
    
    def get_engine(self):
        return self.engine
    
    