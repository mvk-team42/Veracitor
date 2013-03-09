from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from crawler.xpaths import Xpaths
from crawler.items import ArticleItem, ArticleLoader
from crawler.spiders.articleSpider import ArticleSpider
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse


class NewspaperSpider(CrawlSpider):
    name = "newspaper"

    def __init__(self, *args, **kwargs):
        domain = kwargs.get('domain')
        self.start_urls = ["http://" + domain]
        self.rules = (
            Rule(SgmlLinkExtractor(allow_domains=domain, deny=["blogg", "webbtv"]), callback="scrape_article"),
        )
        super(NewspaperSpider, self).__init__()

    def scrape_article(self, response):
        if self._is_article(response):
            return ArticleSpider.scrape_article(response)
        
    def _is_article(self, response):
        xpaths = Xpaths('crawler/webpages.xml')
        domain = urlparse(response.url)[1]
        hxs = HtmlXPathSelector(response)
        for xpath in xpaths.get_article_qualification_xpaths(domain):
            if len(hxs.select(xpath)) > 0:
                return True
        return False
        
        
        
        
        
        
        
        
        
        
        
        
        
        
