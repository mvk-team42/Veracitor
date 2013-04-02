from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse
from os.path import realpath, dirname
from scrapy import log

from ..xpaths import Xpaths
from ..items import ArticleItem, ArticleLoader


class ArticleSpider(BaseSpider):
    name = "article"

    def __init__(self, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls').split(',')

    def parse(self, response):
       return ArticleSpider.scrape_article(response)
        
    @staticmethod
    def scrape_article(response):
        current_dir = dirname(realpath(__file__))
        xpaths = Xpaths(current_dir + '/../webpageXpaths.xml')
        domain = urlparse(response.url)[1]
        loader = ArticleLoader(item=ArticleItem(), response=response)
        
        
        for field in ArticleItem.fields.iterkeys():
            log.msg("field: " + field)
            for xpath in xpaths.get_article_xpaths(field, domain):
                loader.add_xpath(field, xpath)
        loader.add_value("url", response.url)
                
        return loader.load_item()
