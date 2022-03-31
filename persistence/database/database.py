from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from persistence.database.database_objects import Base

try:
    pass
except Exception:
    pass
engine = create_engine('sqlite:///jogoteca.db', echo=False,
                       connect_args={"check_same_thread": False})

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)