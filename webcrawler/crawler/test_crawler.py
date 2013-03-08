#!/usr/bin/env python2.7
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
import scrapy.signals as signals 
from scrapy import log
from crawler.spiders.articleSpider import ArticleSpider

def setup_crawler(domain):
    spider = ArticleSpider(start_urls=domain)
    crawler = Crawler(Settings())
    crawler.configure()
    crawler.crawl(spider)
    crawler.signals.connect(output, signals.item_scraped)
    crawler.start()

def output(item, response, spider):
    print "here!"
    print item
    

for domain in ['http://www.dn.se/nyheter/varlden/nordkorea-upphaver-vapenvila-med-syd', 'http://www.nytimes.com/2013/03/08/world/europe/pope-wanted-must-possess-magnetic-charm-and-grit.html']:
    setup_crawler(domain)
log.start()
reactor.run()
