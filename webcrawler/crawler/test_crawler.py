#!/usr/bin/env python2.7
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from crawler.spiders.articleSpider import ArticleSpider

def setup_crawler(domain):

    # connect signals from spiders to methods
    dispatcher.connect(_item_passed, signal=signals.item_scraped)
    dispatcher.connect(_spider_opened, signal=signals.spider_opened)

    # init spider and send away!
    spider = ArticleSpider(start_urls=domain)
    crawler = Crawler(Settings())
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
