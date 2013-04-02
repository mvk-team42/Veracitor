from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from urlparse import urlparse
from os.path import realpath, dirname
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
        current_dir = dirname(realpath(__file__))
        xml_file = current_dir + '/../webpages.xml'
        tree = ET.parse(xml_file)
        webpages = tree.getroot()
        url = response.url
        domain = url
        already_in_xml = len(webpages.findall("./webpage[@domain='" + domain + "']")) > 0
        
        xpaths = Xpaths(current_dir + '/../webpageXpaths.xml')
        hxs = HtmlXPathSelector(response)
        
        name = self.extract_name(domain, hxs, xpaths).strip()
        rss_link = self.extract_rss_link(domain, hxs, xpaths)
        
        if not already_in_xml:
            webpages.append(ET.Element("webpage", attrib={'domain':domain, 'name':name, 'rss':rss_link}))
            tree.write(xml_file)
        if not extractor.contains_producer(url): #db-method
            new_producer = producer.Producer(name = name,
                description = "No description",
                url = url,
                infos = [],
                source_ratings = [],
                info_ratings = [],
                type_of = "Newspaper")
            new_producer.save()
                           
    def extract_name(self, domain, hxs, xpaths):
        for name_xpath in xpaths.get_webpage_xpaths("name", domain):
            names = hxs.select(name_xpath)
            if len(names) > 0:
                return names[0].extract()
        return "Failed in meta"
                
    def extract_rss_link(self, domain, hxs, xpaths):
        for rss_xpath in xpaths.get_webpage_xpaths("rss-link", domain):
            rss_links = hxs.select(rss_xpath)
            if len(rss_links) > 0:
                return rss_links[0].extract()
        return "Failed in meta"
        
        
        
        
        
       
  
