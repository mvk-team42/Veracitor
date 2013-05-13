from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse
from os.path import realpath, dirname
from scrapy import log
from scrapy.http.response.text import *
from scrapy.utils.python import unicode_to_str
import urllib2 

from ..webpageMeta import WebpageMeta
from ..items import ArticleItem, ArticleLoader
from ....database import *
from .metaNewspaperSpider import MetaNewspaperSpider




class ArticleSpider(BaseSpider):

    """
        Crawls a number of articles. (Mostly just one)
        
        The article-urls are given as kwargs in __init__
    """

    name = "article"

    def __init__(self, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]

    def parse(self, response):
        if ArticleSpider.is_article(response):
            return ArticleSpider.scrape_article(response)
        
    @staticmethod
    def scrape_article(response):
        current_dir = dirname(realpath(__file__))
        meta = WebpageMeta(current_dir + '/../webpageMeta.xml')
        domain = urlparse(response.url)[1]
        loader = ArticleLoader(item=ArticleItem(), response=response)
        
        mainpage_domain = "http://" + urlparse(response.url)[1]
        log.msg("page: "+str(mainpage_domain))
        if not extractor.contains_producer_with_url(mainpage_domain):
            # Construct a response object and send to scrape_meta
            mainpage_body = urllib2.urlopen(mainpage_domain).read()
            mainpage_response = TextResponse(url=mainpage_domain,body=unicode_to_str(mainpage_body, 'utf-8'),encoding='utf-8')
            yield MetaNewspaperSpider.scrape_meta(mainpage_response)
        
        for field in ArticleItem.fields.iterkeys():
            #log.msg("field: " + field)
            for xpath in meta.get_article_xpaths(field, domain):
                log.msg("Xpath for field: "+unicode(field)+" "+unicode(xpath))
                loader.add_xpath(field, xpath)
        loader.add_value("url", response.url)
                
        yield loader.load_item()
