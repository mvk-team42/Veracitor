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
import xml.etree.ElementTree as ET


class MetaNewspaperSpider(BaseSpider):
    name = "metaNewspaper"
    

    def __init__(self, *args, **kwargs):
        url = domain = kwargs.get('url')
        
        self.start_urls = [url]
        super(MetaNewspaperSpider, self).__init__()
        

    def parse(self, response):
        xml_file = "crawler/webpages.xml"
        tree = ET.parse(xml_file)
        webpages = tree.getroot()
        url = response.url
        already_in_xml = len(webpages.findall("./webpage[@domain='" + url + "']")) > 0
        if not already_in_xml:
            webpages.append(ET.Element("webpage", attrib={'domain':url, 'name':url, 'rss':url}))
            tree.write(xml_file)
        
       
  
