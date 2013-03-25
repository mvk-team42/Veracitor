from crawler.spiders.newspaperBankSpider import NewspaperBankSpider
from crawler.spiders.metaNewspaperSpider import MetaNewspaperSpider
from crawler.spiders.rssSpider import RssSpider
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
import xml.etree.ElementTree as ET

from scrapy.signalmanager import SignalManager

from scrapy.crawler import CrawlerProcess
from multiprocessing import Process


def createNewspaperBank():
    _run_spider(NewspaperBankSpider())

def addNewspaper(url):
    _run_spider(MetaNewspaperSpider(url=url))

def requestScrape(newspaper):
    _run_spider(NewspaperSpider(domain=newspaper))

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
    crawler = CrawlerProcess(settings)
    crawler.install()
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
