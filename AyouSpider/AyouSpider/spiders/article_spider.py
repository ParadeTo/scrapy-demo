# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags

from scrapy_redis.spiders import RedisCrawlSpider
from AyouSpider.settings import SQL_DATETIME_FORMAT
from AyouSpider.tools.tools import get_md5, get_datetime


class Article(scrapy.Item):
    title = scrapy.Field()
    website_id = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    content = scrapy.Field()
    publish_time = scrapy.Field()
    create_time = scrapy.Field()


class ArticleSpider(RedisCrawlSpider):

    def __init__(self, website):
        self.name = website.spider_name
        self.redis_key = website.spider_name + ":start_urls"

        self.website = website
        self.allowed_domains = website.allow_domains.split(";")
        self.start_urls = website.start_urls.split(";")

        rule_list = []
        rules_to_follow = website.rules_to_follow.split(";")
        rules_to_parse = website.rules_to_parse.split(";")
        rule_list.append(
            Rule(LinkExtractor(allow=rules_to_parse), follow=True, callback='parse_detail')
        )
        rule_list.append(
            Rule(LinkExtractor(allow=rules_to_follow), follow=True)
        )

        self.rules = tuple(rule_list)
        super(ArticleSpider, self).__init__()

    def parse_detail(self, response):
        now = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        article = Article()
        article["url"] = response.url
        article["url_object_id"] = get_md5(response.url)

        title = response.css(self.website.title_css).extract_first()
        article["title"] = (title if title else '').strip()
        content = remove_tags(response.css(self.website.content_css).extract_first())
        article["content"] = (content if content else '').strip()
        article["website_id"] = self.website.id

        publish_time = response.css(self.website.publish_time_css).extract_first()
        if publish_time:
            publish_time = get_datetime(publish_time)
        article["publish_time"] =  publish_time if publish_time else now

        article["create_time"] =  datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        return article
