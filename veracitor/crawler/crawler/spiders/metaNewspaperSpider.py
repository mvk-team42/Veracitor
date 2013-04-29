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
from ..items import ArticleItem, ArticleLoader
from .articleSpider import ArticleSpider
from ....database import *


class MetaNewspaperSpider(BaseSpider):
    """
        Crawls meta information about newspaper webpage
        
        The newspaper base url is given (without http) as kwarg in __init__
    """

    name = "metaNewspaper"
    

    def __init__(self, *args, **kwargs):
        url = domain = kwargs.get('url')
        self.start_urls = [url]
        super(MetaNewspaperSpider, self).__init__()
        

    def parse(self, response):
        MetaNewspaperSpider.scrape_meta(response)

    @staticmethod
    def scrape_meta(response):
        current_dir = dirname(realpath(__file__))
        xml_file = current_dir + '/../webpageMeta.xml'
        tree = ET.parse(xml_file)
        webpages = tree.getroot()
        url = response.url
        domain = url
        already_in_xml = len(webpages.findall("./webpage[@domain='" + domain + "']")) > 0
        
        meta = WebpageMeta(current_dir + '/../webpageMeta.xml')
        hxs = HtmlXPathSelector(response)
        
        name = MetaNewspaperSpider.extract_name(domain, hxs, meta)
        if name=="" or extractor.contains_producer_with_name(name):
            name = url

        rss_urls = MetaNewspaperSpider.extract_rss_urls(domain, hxs, meta)
        description = MetaNewspaperSpider.extract_description(domain, hxs, meta)
        
        webpage = None

        if already_in_xml:   # Get element and remove existing url-links
            webpage = webpages.find("webpage[@domain='"+domain+"']")
            webpage.remove(webpage.find("rss-urls"))
        else:  # Create new element
            webpage = ET.Element("webpage", attrib={'domain':domain, 'name':name})
        rss_urls_tag = ET.Element("rss-urls")
        for rss_url in rss_urls:  # Add all urls to rss-urls element
            rss = ET.Element("rss")
            rss.text = rss_url
            rss_urls_tag.append(rss)
        webpage.append(rss_urls_tag)  # Append rss-urls to webpage element
        if not already_in_xml:
            webpages.append(webpage)
        tree.write(xml_file)

        if not extractor.contains_producer_with_url(url): #db-method
            new_producer = producer.Producer(name = name,
                description = description,
                url = url,
                infos = [],
                source_ratings = [],
                info_ratings = [],
                type_of = "Newspaper")
            new_producer.save()

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
        
       
  
