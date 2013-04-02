from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse
from ..xpaths import Xpaths
from ..items import ArticleItem, ArticleLoader, ProducerItem
from .articleSpider import ArticleSpider



class NewspaperBankSpider(CrawlSpider):
    name = "newspaperBank"

    def __init__(self, *args, **kwargs):
        
        #self.start_urls = ["http://www.listofnewspapers.com/en/europe/newspapers-in-west-midlands.html"]
        
        self.start_urls = [
                    "http://www.listofnewspapers.com/en/europe/english-newspapers-in-united-kingdom.html",
                    "http://www.listofnewspapers.com/en/europe/swedish-newspapers-in-sweden.html",
                    "http://www.listofnewspapers.com/en/north-america/usa-newspapers-in-united-states-of-america.html",
                    ]
                
        
        
        domain = "http://www.listofnewspapers.com"
        self.rules = (
            Rule(
                SgmlLinkExtractor(restrict_xpaths = "//li[@class='linewspaper']", deny_domain=domain),
                callback = "parse_webpage_link"
            ),
            Rule(
                SgmlLinkExtractor(restrict_xpaths = "//li[@class='linewspaper']"), 
            ),
        )
        super(NewspaperBankSpider, self).__init__(*args, **kwargs)
        
    def parse_webpage_link(self, response):
        return ProducerItem(url = response.url)
        
