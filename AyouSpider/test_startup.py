import logging
import AyouSpider.settings as _settings

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from twisted.internet import reactor

from AyouSpider.model.config import DBSession, Redis
from AyouSpider.model.website import Website
from AyouSpider.spiders.article_spider import ArticleSpider

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
settings.setdict('{"ITEM_PIPELINES":{"AyouSpider.pipelines.MysqlPipeline": 300}}')
# settings.setdict('{"ITEM_PIPELINES":{"scrapy_redis.pipelines.RedisPipeline": 300}}')
settings.set("SCHEDULER_PERSIST", True)
settings.set("SCHEDULER", "scrapy_redis.scheduler.Scheduler")
settings.set("DUPEFILTER_CLASS", "scrapy_redis.dupefilter.RFPDupeFilter")
# settings.setdict('{"ITEM_PIPELINES":{"AyouSpider.AyouSpider.scrapy_redis.pipelines.RedisPipeline": 300}}')
# settings.setdict('{"ITEM_PIPELINES":{"AyouSpider.AyouSpider.scrapy_redis.pipelines.RedisPipeline": 300}}')

db = DBSession()

class Website():
    def __init__(self):
        self.allow_domains = 'news.uuu9.com'
        self.start_urls = 'http://news.uuu9.com/List/List_1414.shtml'
        self.rules_to_follow = '.*\/List\/List_1414.shtml'
        self.rules_to_parse = '.*\/\d+\/\d+.shtml'
        self.title_css = '.robing_con.cl h1::text'
        self.content_css = '#content'
        self.id = 1
        self.publish_time_css = '.robing_con.cl h4::text'

website = Website()

Redis.lpush('article_spider:start_urls', website.start_urls)

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
