from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from AyouSpider.model.config import DBSession, Redis
from AyouSpider.model.website import Website
from AyouSpider.spiders.article_spider import ArticleSpider

settings = Settings()

# crawl settings
settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")
settings.setdict('{"REDIS_PARAMS":{"password": "123456"}}')
settings.setdict('{"ITEM_PIPELINES":{"AyouSpider.pipelines.MysqlPipeline": 300}}')
# settings.setdict('{"ITEM_PIPELINES":{"scrapy_redis.pipelines.RedisPipeline": 300}}')
settings.set("SCHEDULER_PERSIST", True)
settings.set("DEPTH_LIMIT", 3)
settings.set("SCHEDULER", "scrapy_redis.scheduler.Scheduler")
settings.set("DUPEFILTER_CLASS", "scrapy_redis.dupefilter.RFPDupeFilter")

db = DBSession()
crawler = CrawlerProcess(settings)
websites = db.query(Website).filter(Website.enable == 1)
for website in websites:
    Redis.lpush(website.spider_name + ':start_urls', website.start_urls)
    crawler.crawl(ArticleSpider, website)
crawler.start()

