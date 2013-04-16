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
    """
        setup module. Should only be called once [??? Varifrån kommer denna anropas ???]
    """
    #global callback
    #callback = callback_method
    dispatcher.connect(item_scraped , signals.item_scraped)
    log.start()
    
    
def item_scraped(item, response, spider):
    """
        Callback function used internally.
    """
    if isinstance(spider, NewspaperBankSpider):
        add_newspaper(item['url']) #, "-1")
        '''
    if isinstance(spider, ArticleSpider):
        callback(item) #, spider.job_id)
    if isinstance(spider, MetaNewspaperSpider):
        callback(item) #, spider.job_id)
    if isinstance(spider, NewspaperSpider):
        callback(item) #, spider.job_id)
        '''


def create_newspaper_bank():
    """
        Start a celery task that creates our newspaper bank. 
        
        The "newspaper bank" is simply a collection of known newspapers
        with known information such as attribute-xpaths,that are continuosly 
        scraped for new articles
    """
    _run_spider(NewspaperBankSpider())

def add_newspaper(url):
    """
        Start a celery task that adds newspaper with given base-url to 
        the "newspaper bank".
        
        example: url for DN=www.dn.se, url for theGuardian=www.guardian.co.uk
    """
    spider = MetaNewspaperSpider(url=url)
    #spider.job_id = job_id
    _run_spider(spider)
    
def scrape_article(url):
    """
        Start a celery task that scrapes article on given url and adds an Information-object
        to database.
    """
    logger.log("blablabla",logger.Level.debug, logger.Area.crawler)
    spider = ArticleSpider(start_urls=url)
    #spider.job_id = job_id
    _run_spider(spider)

def request_scrape(newspaper):
    """
        Start a celery task that searches the webpage of given newspaper for articles,
        scrapes the articles found (if they're not already stored) and adds Information-objects
        to database.
    """
    spider = NewspaperSpider(domain=newspaper)
    #spider.job_id = job_id
    _run_spider(spider)

def startContinuousScrape():
    """ 
        Start a celery task whose job is to loop through the newspaperbank and scrape the 
        newspapers for new articles and, if they're not already stored, store Information-
        objects in the database.
    
    """
    newspaper_urls = []
    xml_file = "crawler/webpages.xml"
    tree = ET.parse(xml_file)
    webpages = tree.getroot().findall("./webpage")
    for webpage in webpages:
        newspaper_urls.append(webpage.get("domain"))
    while (True):
        for url in newspaper_urls:
            print url
            
            print tree.getroot().findall("//webpage[@domain="+url+"]/rss")
            
            #for rss_link in rss_links:
            #    spider = RssSpider(url="http://www.dn.se/m/rss/senaste-nytt")
            #_run_spider(spider)
            

def stopContinuousScrape():
    pass
    
    
def _run_spider(spider):
    """ private method to reduce boilerplate """
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
