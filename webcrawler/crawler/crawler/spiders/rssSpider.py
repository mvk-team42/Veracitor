from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import XmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from crawler.xpaths import Xpaths
from crawler.items import ArticleItem, ArticleLoader
from crawler.spiders.articleSpider import ArticleSpider
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse
from pprint import pprint

class RssSpider(CrawlSpider):
    name = "rss"
   
    def __init__(self, *args, **kwargs):
        self.xpaths = Xpaths('crawler/webpages.xml')
        #self.start_urls = [kwargs.get('url')]
        self.start_urls = ["http://www.guardian.co.uk/world/zimbabwe/rss"]
        super(RssSpider, self).__init__()
        
    def parse(self, response):
        hxs = XmlXPathSelector(response)
        items = []
        for item in hxs.select('//item'):
            items.append(ArticleItem())
            if len(item.select("title")) > 0:
                items[-1]["title"] = item.select("title/text()")[0].extract()  
            if len(item.select("pubDate")) > 0:
                items[-1]["date"] =  item.select("pubDate/text()")[0].extract()
            if len(item.select("link")) > 0:
                print item.select("link/text()").extract()
                items[-1]["url"] = item.select("link")[0].extract()
            if len(item.select("description")) > 0:
                items[-1]["summary"] = item.select("description/text()")[0].extract()   
        return items
            
            
        
        
        
        
        
        
