
#!/usr/bin/env python2.7
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from crawler.spiders.articleSpider import ArticleSpider


# import settings
from scrapy.utils.project import get_project_settings

import crawler.settings as default_settings

def setup_crawler(domain):
    spider = NewspaperSpider(domain=domain)
    dispatcher.connect(_spider_closed, signal=signals.spider_closed)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

def _spider_closed(spider):
    print "SPIDER CLOSED: " + str(spider)


setup_crawler("www.dn.se")
log.start()
reactor.run()
