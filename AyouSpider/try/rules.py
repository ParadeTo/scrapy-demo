# -*- coding: utf-8 -*-
from AyouSpider.AyouSpider.model.config import DBSession
from AyouSpider.AyouSpider.model.website import Website

db = DBSession()

websites = db.query(Website)
for website in websites:
    print(website)