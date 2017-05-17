# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

# 初始化数据库连接:
engine = create_engine('mysql+mysqldb://root:123456@localhost:3306/scrapy-demo?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 初始化redis数据库连接
Redis = redis.StrictRedis(host='localhost',port=6379,db=0,password=123456)