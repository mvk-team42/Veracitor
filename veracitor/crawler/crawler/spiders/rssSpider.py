from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import XmlXPathSelector, HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse
from pprint import pprint
from scrapy.http import Request
from os.path import realpath, dirname

from ..webpageMeta import WebpageMeta
from ..items import ArticleItem, ArticleLoader
from .articleSpider import ArticleSpider


class RssSpider(CrawlSpider):

    """
        Scrapes all articles in given RSS-page (that belongs to a specific newspaper)
        Constructs Article-items just as ArticleSpider and NewspaperSpider, but probably quicker
        since all info is neatly organized in XML.
    """

    name = "rss"
   
    def __init__(self, *args, **kwargs):
        #self.xpaths = Xpaths(current_dir + '/../webpages.xml')
        self.start_urls = [kwargs.get('url')]
        super(RssSpider, self).__init__()
        
    def parse(self, response):
        xxs = XmlXPathSelector(response)
        items = []
        requests = []
        for item_tag in xxs.select('//item'):
            items.append(ArticleItem())
            if len(item_tag.select("title")) > 0:
                items[-1]["title"] = item_tag.select("title/text()")[0].extract()  
            if len(item_tag.select("pubDate")) > 0:
                items[-1]["time_published"] =  item_tag.select("pubDate/text()")[0].extract()
            if len(item_tag.select("link")) > 0:
                items[-1]["url"] = item_tag.select("link/text()")[0].extract()
            if len(item_tag.select("description")) > 0:
                items[-1]["summary"] = item_tag.select("description/text()")[0].extract()   
            
            request = Request(items[-1]["url"], callback=self.extract_author_from_link)
            request.meta["item"] = items[-1]
            yield request
   
    def extract_author_from_link(self, response):
        current_dir = dirname(realpath(__file__))
        meta = WebpageMeta(current_dir + '/../webpageMeta.xml')
        domain = urlparse(response.url)[1]
        hxs = HtmlXPathSelector(response)
        for xpath in meta.get_article_xpaths("publishers", domain):
                author = hxs.select(xpath).extract()
                if len(author) > 0 and author[0].strip() != "":
                    response.meta["item"]["publishers"] = author[0]
                    return response.meta["item"]   
        return response.meta["item"]

            
            
        
        
        
        
        
        
