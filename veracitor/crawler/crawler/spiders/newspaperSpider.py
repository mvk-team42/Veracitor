from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy import log
from urlparse import urlparse
from os.path import realpath, dirname

from ..xpaths import Xpaths
from ..items import ArticleItem, ArticleLoader
from .articleSpider import ArticleSpider



class NewspaperSpider(CrawlSpider):

    """
        Looks for articles everywhere on a given newspaper webpage and when finding one, 
        uses ArticleSpider's methods to scrape it, and then sends it to pipeline for 
        further processing.
    """

    name = "newspaper"
    

    def __init__(self, *args, **kwargs):
        current_dir = dirname(realpath(__file__))
        self.xpaths = Xpaths(current_dir + '/../webpageXpaths.xml')
        domain = kwargs.get('domain')
        log.msg("crawling domain " + domain)
        self.start_urls = [domain]
        domain = domain.replace('http://','')
        self.rules = (
            Rule(
                SgmlLinkExtractor(allow_domains=domain, deny=self.xpaths.get_article_deny_urls(domain)), 
                callback="scrape_article"
            ),
        )
        super(NewspaperSpider, self).__init__()


    def scrape_article(self, response):
        log.msg("inside scrape_article")
        if self._is_article(response):
            return ArticleSpider.scrape_article(response)

    def _is_article(self, response):
        domain = urlparse(response.url)[1]
        hxs = HtmlXPathSelector(response)
        for xpath in self.xpaths.get_article_qualification_xpaths(domain):
            if len(hxs.select(xpath)) > 0:
                return True
        return False
        
        
        
        
        
        
        
        
        
        
        
        
        
        
