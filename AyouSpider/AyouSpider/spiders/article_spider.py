# -*- coding: utf-8 -*-
from AyouSpider.AyouSpider.scrapy_redis.spiders import RedisCrawlSpider


class ArticleSpider(RedisCrawlSpider):
    name = 'article_spider'
    redis_key = 'article_spider:start_urls'


