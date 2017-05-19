# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from AyouSpider.AyouSpider.scrapy_redis.spiders import RedisCrawlSpider
from AyouSpider.AyouSpider.settings import SQL_DATETIME_FORMAT
from AyouSpider.AyouSpider.tools.tools import get_md5


class Article(scrapy.Item):
    title = scrapy.Field()
    website_id = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    content = scrapy.Field()
    publish_time = scrapy.Field()
    create_time = scrapy.Field()

class ArticleSpider(RedisCrawlSpider):
    name = 'article_spider'
    redis_key = 'article_spider:start_urls'

    def __init__(self, website):
        self.website = website
        self.allowed_domains = website.allow_domains.split(";")
        self.start_urls = website.start_urls.split(";")

        rule_list = []
        rules_to_follow = website.rules_to_follow.split(";")
        rules_to_parse = website.rules_to_parse.split(";")
        rule_list.append(
            Rule(LinkExtractor(allow=rules_to_follow), follow=True)
        )
        rule_list.append(
            Rule(LinkExtractor(allow=rules_to_parse), follow=True, callback='parse_detail')
        )
        self.rules = tuple(rule_list)
        super(ArticleSpider, self).__init__()

    def parse_detail(self, response):
        article = Article()
        article["url"] = response.url
        article["url_object_id"] = get_md5(response.url)
        article["title"] = response.css(self.website.title_css).extract_first()
        article["content"] = response.css(self.website.content_css).extract_first()
        article["website_id"] = self.website.id
        article["publish_time"] =  response.css(self.website.publish_time_css).extract_first()
        article["create_time"] =  datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        return article
