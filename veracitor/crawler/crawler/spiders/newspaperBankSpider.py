from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy import log
from urlparse import urlparse

from ..webpageMeta import WebpageMeta
from ..items import ArticleItem, ArticleLoader, ProducerItem
from .articleSpider import ArticleSpider
from .metaNewspaperSpider import MetaNewspaperSpider



class NewspaperBankSpider(CrawlSpider):

    """
        Crawls webpages containing lists of newspapers and adds them to our "newspaper bank"
    """


    name = "newspaperBank"

    def __init__(self, *args, **kwargs):
        
        
        self.start_urls = [
                    "http://www.listofnewspapers.com/en/europe/english-newspapers-in-united-kingdom.html",
                    "http://www.listofnewspapers.com/en/europe/swedish-newspapers-in-sweden.html",
                    "http://www.listofnewspapers.com/en/north-america/usa-newspapers-in-united-states-of-america.html",
                    ]
 
        domain = "www.listofnewspapers.com"

        self.rules = (
            Rule(
                SgmlLinkExtractor(restrict_xpaths = "//li[@class='linewspapers']", deny_domains=domain),
                callback = "parse_webpage_link"
            ),
            Rule(
                SgmlLinkExtractor(restrict_xpaths = "//li[@class='linewspapers']", allow_domains=domain)
            ),
        )
        log.msg("initiated")
        super(NewspaperBankSpider, self).__init__(*args, **kwargs)
     
        
    def parse_webpage_link(self, response):
        log.msg("found link")
        return MetaNewspaperSpider.scrape_meta(response)
