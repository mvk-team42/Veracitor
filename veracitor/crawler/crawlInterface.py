# -*- coding: utf-8 -*-

""" 
.. module:: crawlInterface
    :synopsis: The interface for the webcrawler package

.. moduleauthor:: Gustaf Lindstedt <glindste@kth.se>
.. moduleauthor:: Jonathan Murray <jmu@kth.se>
"""

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
from os.path import realpath, dirname

from .crawler.spiders.newspaperBankSpider import NewspaperBankSpider
from .crawler.spiders.metaNewspaperSpider import MetaNewspaperSpider
from .crawler.spiders.rssSpider import RssSpider
from .crawler.spiders.articleSpider import ArticleSpider
from .crawler.spiders.newspaperSpider import NewspaperSpider
from .crawler.webpageMeta import WebpageMeta
from ..logger import logger


def init_interface():
    """
    Setup module. Should only be called once.

    Connects signals and starts the scrapy logger.

    Returns:
        None
    """
    #global callback
    #callback = callback_method
    dispatcher.connect(_item_scraped , signals.item_scraped)
    log.start()


def _item_scraped(item, response, spider):
    """
    Callback function used internally.
    """


def create_newspaper_bank():
    """
    Start a celery task that creates our newspaper bank.

    The "newspaper bank" is simply a collection of known newspapers
    with known information such as attribute-xpaths,that are continuosly
    scraped for new articles.

    Returns:
        None
    """
    _run_spider(NewspaperBankSpider())

def add_newspaper(url):
    """
    Start a celery task that adds newspaper with given base-url to
    the "newspaper bank".

    Args:
        url (str): The base-url for the source to be added. Example url for DN=www.dn.se, url for theGuardian=www.guardian.co.uk .

    Returns:
        None
    """
    spider = MetaNewspaperSpider(url=_httpify(url))
    #spider.job_id = job_id
    _run_spider(spider)

def scrape_article(url):
    """
    Start a celery task that scrapes article on given url and adds an Information-object
    to database.

    Args:
        url (str): The url for the article to be added.

    Returns:
        None
    """
    #logger.log("blablabla",logger.Level.debug, logger.Area.crawler)
    spider = ArticleSpider(start_url=_httpify(url))
    #spider.job_id = job_id
    _run_spider(spider)

def request_scrape(newspaper_url):
    """
    Start a celery task that searches the webpage of given newspaper for articles,
    scrapes the articles found (if they're not already stored) and adds Information-objects
    to database.

    Args:
        newspaper_url (str): The base-url of the newspaper that is to be scraped.

    Returns:
        None
    """
    spider = NewspaperSpider(domain=_httpify(newspaper_url))
    #spider.job_id = job_id
    _run_spider(spider)

def start_continuous_scrape():
    """
    Start a celery task whose job is to loop through the newspaperbank and scrape the
    newspapers for new articles and, if they're not already stored, store Information-
    objects in the database.

    Returns:
        None

    """
    current_dir = dirname(realpath(__file__))
    xml_file = current_dir + "/crawler/webpageMeta.xml"
    meta = WebpageMeta(xml_file)

    newspaper_urls = meta.get_all_webpage_domains()

    for url in newspaper_urls:
        log.msg(url)

        spider_has_run = False  # om rss failar ska man koera request_scrape
        for rss_url in meta.get_rss_urls(url):
            spider = RssSpider(url=_httpify(rss_url))
            _run_spider(spider)
            spider_has_run = True
            log.msg("Rss link found")

        if not spider_has_run:
            request_scrape(url)

def test_rss(url):
    spider = RssSpider(url=_httpify(url))
    _run_spider(spider)


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

def _crawl(crawler, spider):
    crawler.crawl(spider)
    crawler.start()
    crawler.stop()



def _httpify(url):
    if url.startswith("http://"):
        return url
    return "http://" + url



if __name__ == "__main__":
    startContinuousScrape()
