from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "postgresql://postgres:rootAdmin@localhost/myFastApi"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# try:
#     conn = connect(host="localhost", database="myFastApi",
#                    user="postgres", password="rootAdmin", cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("database connection succesfull")
# except Exception as err:
#     print("problem with connection")
#     print(err)
