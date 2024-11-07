from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from wtforms.validators import DataRequired, URL, Email, Length
from sqlalchemy import Integer, String, Text
from flask_login import UserMixin

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    surname: Mapped[str] = mapped_column(Text, nullable=False)
    login: Mapped[str] = mapped_column(String(20), nullable=False, unique=True) 
    password: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(String(20), nullable=False) 
    telegramId: Mapped[int] = mapped_column(BigInteger, default=-1)
    registeredAt: Mapped[str] = mapped_column(String, nullable=False)
    isAdmin: Mapped[bool] = mapped_column(Boolean, default=False)

class Passphrase(Base):
    __tablename__ = "passphrases"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phrase: Mapped[str] = mapped_column(String(64), nullable=False, unique=True) 
    user: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))


class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article: Mapped[str] = mapped_column(Text, nullable=False)
    publishAt: Mapped[str] = mapped_column(String, nullable=False)