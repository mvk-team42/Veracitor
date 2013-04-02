from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse
import xml.etree.ElementTree as ET

from ..xpaths import Xpaths
from ..items import ArticleItem, ArticleLoader
from .articleSpider import ArticleSpider
from ....database import *


class MetaNewspaperSpider(BaseSpider):
    name = "metaNewspaper"
    

    def __init__(self, *args, **kwargs):
        url = domain = kwargs.get('url')
        self.start_urls = ["http://" + url]
        super(MetaNewspaperSpider, self).__init__()
        

    def parse(self, response):
        xml_file = "crawler/webpages.xml"
        tree = ET.parse(xml_file)
        webpages = tree.getroot()
        url = response.url
        domain = url
        already_in_xml = len(webpages.findall("./webpage[@domain='" + domain + "']")) > 0
        
        Xpaths xpaths = Xpaths()
        hxs = HtmlXPathSelector(response)
        
        name = self.extract_name(hxs, xpaths)
        rss_link = self.extract_rss_link(hxs, xpaths)
        
        if not already_in_xml:
            webpages.append(ET.Element("webpage", attrib={'domain':domain, 'name':name, 'rss':rss_link}))
            tree.write(xml_file)
        if not exists_producer(url): #db-method
            new_producer = Producer(name = url, description = "No description")
            new_producer.save()
                           
    def extract_name(self, hxs, xpaths):
        for name_xpath in xpaths.get_webpage_xpaths("name", domain):
            names = xpaths.select(name_xpath)
            if len(names) > 0:
                return = names[0].extract()
        return "Failed in meta"
                
    def extract_rss_link(self, hxs, xpaths):
        for rss_xpath in xpaths.get_webpage_xpaths("rss-link", domain):
            rss_links = xpaths.select(rss_xpath)
            if len(rss_links) > 0:
                return = rss_links[0].extract()
        return "Failed in meta"
        
        
        
        
        
       
  
