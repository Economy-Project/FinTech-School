import psycopg2
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    login = Column(String(20), unique = True)

    phash = Column(String(32))
    psalt = Column(String(16))

    telegramId = Column(BigInteger, default = -1)
    
    registeredAt = Column(Integer)

class Passphrase(Base):
    __tablename__ = "passphrases"
    phrase = Column(String(64), primary_key = True)
    user = Column(Integer, ForeignKey("users.id"))

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key = True)
    article = Column(Text)
    publishAt = Column(Integer)


Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)