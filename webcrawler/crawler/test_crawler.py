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

    # connect signals from spiders to methods
    dispatcher.connect(_item_passed, signal=signals.item_scraped)
    dispatcher.connect(_spider_opened, signal=signals.spider_opened)

    # init spider
    spider = ArticleSpider(start_urls=domain)

    # get project settings and use to init crawler
    settings = get_project_settings()
    crawler = Crawler(settings)
    # print "Pipelines enabled: " + "".join(crawler.settings.get('ITEM_PIPELINES'))

    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

def _item_passed(item, response, spider):
    print "here!"
    print item

def _spider_opened(spider):
    print "spider opened!"
    

# insert test articles here
for domain in ['http://www.dn.se/nyheter/varlden/nordkorea-upphaver-vapenvila-med-syd', 'http://www.nytimes.com/2013/03/08/world/europe/pope-wanted-must-possess-magnetic-charm-and-grit.html']:
    setup_crawler(domain)

# stuff
log.start()
reactor.run()
