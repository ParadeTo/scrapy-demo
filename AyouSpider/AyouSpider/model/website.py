# -*- coding: utf-8 -*-

from sqlalchemy import Column, String , DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class Website(Base):
    __tablename__ = 'website'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    name = Column(String)
    spider_name = Column(String)
    allow_domains = Column(String)
    start_urls = Column(String)
    rules_to_follow = Column(String)
    rules_to_parse = Column(String)
    title_css = Column(String)
    content_css = Column(String)
    publish_time_css = Column(String)
    enable = Column(Integer)

    def __str__(self):
        return self.name