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

from crawler.spiders.newspaperBankSpider import NewspaperBankSpider
from crawler.spiders.metaNewspaperSpider import MetaNewspaperSpider
from crawler.spiders.rssSpider import RssSpider
from crawler.spiders.articleSpider import ArticleSpider
from crawler.spiders.newspaperSpider import NewspaperSpider


def set_callbacks(information, producer):
    global information_callback, producer_callback
    information_callback = information
    producer_callback = producer
    dispatcher.connect(item_scraped , signals.item_scraped)
    
    
def item_scraped(item, response, spider):
    if isinstance(spider, NewspaperBankSpider):
        addNewspaper(item.url)
    if isinstance(spider, ArticleSpider):
        information_callback(item, spider.job_id)
    if isinstance(spider, MetaNewspaperSpider):
        producer_callback(item, spider.job_id)
        


def createNewspaperBank():
    _run_spider(NewspaperBankSpider())

def addNewspaper(url, job_id):
    spider = MetaNewspaperSpider(url=url)
    spider.job_id = job_id
    _run_spider(spider)
    
def scrapeArticle(url, job_id):
    spider = ArticleSpider(start_urls=url)
    spider.job_id = job_id
    _run_spider(spider)

def requestScrape(newspaper, job_id):
    spider = NewspaperSpider(domain=newspaper)
    spider.job_id = job_id
    _run_spider(spider)

def startContinuousScrape():
    newspaperUrls = []
    xml_file = "crawler/webpages.xml"
    tree = ET.parse(xml_file)
    webpages = tree.getroot().findall("./webpage")
    for webpage in webpages:
        newspaperUrls.append(webpage.get("url"))
    while (True):
        for url in newspaperUrls:
            print url
            spider = RssSpider(url="http://www.dn.se/m/rss/senaste-nytt")
            _run_spider(spider)
            

def stopContinuousScrape():
    pass
    
    
def _run_spider(spider):
    settings = get_project_settings()
    print settings.getlist("SPIDER_MODULES")
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
