from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import String, Integer, Column, DateTime
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")


engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Information(Base):
    __tablename__ = ("informations")
    __table_args__ = {'extend_existing': True}  # Это позволит переопределить существующую таблицу

    id = Column(Integer, primary_key=True)
    name = Column(String)
    data = Column(String)


class Orders(Base):
    __tablename__ = "orders"
    __table_args__ = {'extend_existing': True}  # Это позволит переопределить существующую таблицу

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    price = Column(Integer)
    profit = Column(Integer)
    sum_profit_all_time = Column(Integer)
    date = Column(DateTime)