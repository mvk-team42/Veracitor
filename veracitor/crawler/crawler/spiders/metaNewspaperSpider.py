from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse
from os.path import realpath, dirname
import xml.etree.ElementTree as ET

from ..webpageMeta import WebpageMeta
from ..items import ArticleItem, ProducerItem, ArticleLoader
from ....database import *


class MetaNewspaperSpider(BaseSpider):
    """
        Crawls meta information about newspaper webpage
        
        The newspaper base url is given (without http) as kwarg in __init__
    """

    name = "metaNewspaper"
    

    def __init__(self, *args, **kwargs):
        url = kwargs.get('url')
        self.start_urls = [url]
        super(MetaNewspaperSpider, self).__init__()
        

    def parse(self, response):
        return MetaNewspaperSpider.scrape_meta(response)

    @staticmethod
    def scrape_meta(response):
    
        producer_item = ProducerItem()

        current_dir = dirname(realpath(__file__))
        meta = WebpageMeta(current_dir + '/../webpageMeta.xml')
        hxs = HtmlXPathSelector(response)
        producer_item["name"] = MetaNewspaperSpider.extract_name(response.url, hxs, meta)
        producer_item["rss_urls"] = MetaNewspaperSpider.extract_rss_urls(response.url, hxs, meta)
        producer_item["description"] = MetaNewspaperSpider.extract_description(response.url, hxs, meta)
        producer_item["url"] = response.url
        producer_item["infos"] = []
        producer_item["source_ratings"] = []
        producer_item["info_ratings"] = []
        producer_item["type_of"] = "newspaper"

        return producer_item
         
         
        
    #These three should be in some ItemLoader, whatever    
        
    @staticmethod
    def extract_name(domain, hxs, meta):
        for name_xpath in meta.get_webpage_xpaths("name", domain):
            names = hxs.select(name_xpath)
            if len(names) > 0:
                return names[0].extract().strip()
        return ""

    @staticmethod
    def extract_rss_urls(domain, hxs, meta):
        for rss_xpath in meta.get_webpage_xpaths("rss-link", domain):
            rss_links = hxs.select(rss_xpath)
            if len(rss_links) > 0:
                return [rss_link.extract().strip() for rss_link in rss_links]
        return []

    @staticmethod
    def extract_description(domain, hxs, meta):
        for description_xpath in meta.get_webpage_xpaths("description", domain):
            descriptions = hxs.select(description_xpath)
            if len(descriptions) > 0:
                return descriptions[0].extract().strip()
        return "No description scraped."
