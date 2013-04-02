from multiprocessing import Process
from twisted.internet import reactor
from scrapy.signalmanager import SignalManager
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from scrapy import log
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from time import time
from scrapy.exceptions import CloseSpider
import xml.etree.ElementTree as ET

from .crawler.spiders.newspaperBankSpider import NewspaperBankSpider
from .crawler.spiders.metaNewspaperSpider import MetaNewspaperSpider
from .crawler.spiders.rssSpider import RssSpider
from .crawler.spiders.articleSpider import ArticleSpider
from .crawler.spiders.newspaperSpider import NewspaperSpider
from ..logger import logger


def init_interface():
    #global callback
    #callback = callback_method
    dispatcher.connect(item_scraped , signals.item_scraped)
    log.start()
    
    
def item_scraped(item, response, spider):
    if isinstance(spider, NewspaperBankSpider):
        add_newspaper(item['url']) #, "-1")
    if isinstance(spider, ArticleSpider):
        callback(item) #, spider.job_id)
    if isinstance(spider, MetaNewspaperSpider):
        callback(item) #, spider.job_id)
    if isinstance(spider, NewspaperSpider):
        callback(item) #, spider.job_id)


def create_newspaper_bank():
    _run_spider(NewspaperBankSpider())

def add_newspaper(url):
    spider = MetaNewspaperSpider(url=url)
    #spider.job_id = job_id
    _run_spider(spider)
    
def scrape_article(url):
    logger.log("blablabla",logger.Level.debug, logger.Area.crawler)
    spider = ArticleSpider(start_urls=url)
    #spider.job_id = job_id
    _run_spider(spider)

def request_scrape(newspaper):
    spider = NewspaperSpider(domain=newspaper)
    #spider.job_id = job_id
    _run_spider(spider)

def startContinuousScrape():
    newspaper_urls = []
    xml_file = "crawler/webpages.xml"
    tree = ET.parse(xml_file)
    webpages = tree.getroot().findall("./webpage")
    for webpage in webpages:
        newspaper_urls.append(webpage.get("url"))
    while (True):
        for url in newspaper_urls:
            print url
            spider = RssSpider(url="http://www.dn.se/m/rss/senaste-nytt")
            _run_spider(spider)
            

def stopContinuousScrape():
    pass
    
    
def _run_spider(spider):
    settings = get_project_settings()
    #print settings.getlist("SPIDER_MODULES")
    crawler = CrawlerProcess(settings)
    #crawler.install()
    crawler.configure()
    p = Process(target=_crawl,args=[crawler,spider])
    p.start()
    p.join()
    #settings = get_project_settings()
    #crawler = Crawler(settings)
    #crawler.configure()
    #crawler.crawl(spider)
    #crawler.start()
    #reactor.run()

def _crawl(crawler, spider):
    crawler.crawl(spider)
    crawler.start()
    crawler.stop()
    
    

   
   
   
   
   
if __name__ == "__main__":
    startContinuousScrape() 
