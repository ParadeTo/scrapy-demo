# -*- coding: utf-8 -*-

from sqlalchemy import Column, String , Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'article'

    url_object_id = Column(String, primary_key=True)
    url = Column(String)
    title = Column(String)
    content = Column(String)
    website_id = Column(Integer)
    publish_time = Column(DateTime)
    create_time = Column(DateTime)