import logging
import AyouSpider.AyouSpider.settings as _settings

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from twisted.internet import reactor

from AyouSpider.AyouSpider.model.config import DBSession
from AyouSpider.AyouSpider.model.website import Website
from AyouSpider.AyouSpider.spiders.article_spider import ArticleSpider

RUNNING_CRAWLERS = []

def spider_closing(spider):
    """Activates on spider closed signal"""
    logging.log(logging.INFO, "Spider closed: %s" % spider)
    RUNNING_CRAWLERS.remove(spider)
    if not RUNNING_CRAWLERS:
        reactor.stop()


settings = Settings()

# crawl settings
settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")
settings.setdict('{"REDIS_PARAMS":{"password": "123456"}}')

db = DBSession()

class Website():
    def __init__(self):
        self.allow_domains = 'news.uuu9.com'
        self.start_urls = 'http://www.uuu9.com/'
        self.rules_to_follow = '.*'
        self.rules_to_parse = '\/\d+\/\d+.shtml'
        self.title_css = '.robing_con.c1 h1::text'
        self.content_css = '#content'
        self.id = 1
        self.publish_time_css = '.robing_con.c1 h4::text'

website = Website()

# website.allow_domains = 'news.uuu9.com'
# website.start_urls = 'http://www.uuu9.com/'
# website.rules_to_follow = '.*'
# website.rules_to_parse = '\/\d+\/\d+.shtml'
# website.title_css = '.robing_con.c1 h1::text'
# website.content_css = '#content'
# website.id = 1
# website.publish_time_css = '.robing_con.c1 h4::text'

crawler = CrawlerProcess(settings)
# spider = ArticleSpider(website)  # instantiate every spider using rule
# RUNNING_CRAWLERS.append(spider)

# stop reactor when spider closes
# dispatcher.connect(spider_closing, signal=signals.spider_closed)

crawler.crawl(ArticleSpider, website)
crawler.start()

# blocks process so always keep as the last statement
# reactor.run()
