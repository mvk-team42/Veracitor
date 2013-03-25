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
from xml.etree.ElementTree import ElementTree


class LightNewspaperSpider(BaseSpider):
    name = "lightNewspaper"
    

    def __init__(self, *args, **kwargs):
        url = domain = kwargs.get('url')
        
        self.start_urls = [url]
        super(LightNewspaperSpider, self).__init__()
        

    def parse(self, response):
        tree = ElementTree()
        xml_file = "crawler/webpages.xml"
        webpages = ElementTree.parse(xml_file).getroot().find("//webpages")
        
        
       
  
