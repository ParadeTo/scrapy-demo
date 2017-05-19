import logging
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from twisted.internet import reactor

from AyouSpider.AyouSpider.model.config import DBSession
from AyouSpider.AyouSpider.model.website import Website
from AyouSpider.AyouSpider.spiders.article_spider import ArticleSpider

RUNNING_CRAWLERS = []

def spider_closing(spider):
    """Activates on spider closed signal"""
    logging.log("Spider closed: %s" % spider, logging.INFO)
    RUNNING_CRAWLERS.remove(spider)
    if not RUNNING_CRAWLERS:
        reactor.stop()


settings = Settings()

# crawl settings
settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")

db = DBSession()
websites = db.query(Website).filter(Website.enable == 1)
for website in websites:
    crawler = Crawler(settings)
    spider = ArticleSpider(website)  # instantiate every spider using rule
    RUNNING_CRAWLERS.append(spider)

    # stop reactor when spider closes
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

# blocks process so always keep as the last statement
reactor.run()