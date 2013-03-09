from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from crawler.xpaths import Xpaths
from crawler.items import ArticleItem, ArticleLoader
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse

class NewspaperSpider(CrawlSpider):
    name = "newspaper"

    def __init__(self, *args, **kwargs):
        #super(NewspaperSpider, self).__init__(*args, **kwargs)
        domain = kwargs.get('domain')
        self.start_urls = ["http://" + domain]
        self.rules = (
            Rule(SgmlLinkExtractor(allow_domains=domain, deny=["blogg", "webbtv"]), callback="parse_article"),
        )
        super(NewspaperSpider, self).__init__()

    def parse_article(self, response):
        xpaths = Xpaths('crawler/webpages.xml')
        domain = urlparse(response.url)[1]
        hxs = HtmlXPathSelector(response)
        is_article = False
        for xpath in xpaths.get_article_qualification_xpaths(domain):
            if len(hxs.select(xpath)) > 0:
                is_article = True
                break
                
        if not is_article:
            #print response.url + " - NO!"
            return []
            
        #print response.url + " - YES!"
        
        loader = ArticleLoader(item=ArticleItem(), response=response)
        for field in ArticleItem.fields.iterkeys():
            for xpath in xpaths.get_xpaths(field, domain):
                loader.add_xpath(field, xpath)
        loader.add_value("url", response.url)
                
        return loader.load_item()
        
