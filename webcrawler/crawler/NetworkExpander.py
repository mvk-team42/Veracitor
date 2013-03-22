from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from scrapy import log
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from crawler.spiders.articleSpider import ArticleSpider
from crawler.spiders.newspaperSpider import NewspaperSpider
from time import time
from scrapy.exceptions import CloseSpider

from scrapy.signalmanager import SignalManager


deadline = -1

def stop_reactor():
    reactor.stop()

def add_info(url):
    
    dispatcher.connect(_item_scraped, signal=signals.item_scraped)
    dispatcher.connect(stop_reactor, signal=signals.spider_closed)
    dispatcher.connect(spider_opened, signal=signals.spider_opened)
    
    SignalManager.connect(spider_opened, signal=signals.spider_opened)
    
    spider = ArticleSpider(start_urls=url)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run()
    


def _item_scraped(item, response, spider):
    pass
    # Lagg till info i db, om den inte redan finns 
    # Lagg till kallan i db, om den inte redan finns
    
    """
    global deadline
    if deadline != -1 and time() > deadline:
        deadline = -1
        raise CloseSpider("out of time!")
    """
   
    
def expand_with_references(start_url, max_time):
    global deadline
    deadline = time() + max_time
    spider = NewspaperSpider(domain=start_url)
    dispatcher.connect(_item_scraped, signal=signals.item_scraped)
    dispatcher.connect(stop_reactor, signal=signals.spider_closed)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    #log.start()
    reactor.run()
    
    
if __name__ == "__main__":
    print "main"
    expand_with_references("www.dn.se", 2)

    
