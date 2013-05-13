from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy import log

from ..items import ArticleItem, ArticleLoader
from .articleSpider import ArticleSpider
from .utils import *



class NewspaperSpider(CrawlSpider):

    """
        Looks for articles everywhere on a given newspaper webpage and when finding one, 
        uses ArticleSpider's methods to scrape it, and then sends it to pipeline for 
        further processing.
    """

    name = "newspaper"
    

    def __init__(self, *args, **kwargs):
        domain = kwargs.get('domain')
        log.msg("crawling domain " + domain)
        self.start_urls = [domain]
        domain = domain.replace('http://','')
        self.rules = (
            Rule(
                SgmlLinkExtractor(allow_domains=domain, deny=meta.get_article_deny_urls(domain)), 
                follow=True,
                callback="scrape_article"
            ),
        )
        super(NewspaperSpider, self).__init__()


    def scrape_article(self, response):
        log.msg("inside scrape_article")
        if is_article(response):
            return scrape_article(response)
