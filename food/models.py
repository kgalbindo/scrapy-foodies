from sqlalchemy import create_engine, Column, ForeignKey, PrimaryKeyConstraint, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import food.settings

DeclarativeBase = declarative_base()
  
def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**food.settings.DATABASE))

def create_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)
   
class FoodReview(DeclarativeBase):
    """Sqlalchemy food_review model"""
    __tablename__ = "food_review"
    
    id = Column(Integer, primary_key=True)
    article_id = Column('article_id', Integer)
    article_date = Column('date', DateTime)
    article_title = Column('title', String)
    article_link = Column('link', String)

    article_tag = Column('tag', String)
    scraped_date = Column('scraped_date', DateTime)
    venue_name = Column('venue_name', String)
    review_score = Column('review_score', Float)
    review_pros = Column('review_pros', String, nullable=True)
    
    review_cons = Column('review_cons', String, nullable=True)
    recommended_dish = Column('recommended_dish', String, nullable=True)
    opening_hours = Column('opening_hours', String)
    address = Column('address', String)
    source = Column('source', String)
    article_writer = Column('article_writer', String)