# -*- coding: utf-8 -*-

import re
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import log
from datetime import datetime
from datetime import date
from os.path import dirname, realpath
from urlparse import urlparse
from time import strptime, mktime
import re

from .items import ArticleItem
from .webpageMeta import WebpageMeta
from .spiders.newspaperBankSpider import NewspaperBankSpider
from .spiders.newspaperSpider import NewspaperSpider
from .spiders.metaNewspaperSpider import MetaNewspaperSpider
from .spiders.articleSpider import ArticleSpider
from .spiders.rssSpider import RssSpider
from ...database import *
from ...logger import *
        
def process_producer(producer, spider):

    current_dir = dirname(realpath(__file__))
    xml_file = current_dir + '/webpageMeta.xml'
    tree = ET.parse(xml_file)
    webpages = tree.getroot()
    # Might wanna httpify all uses of producer.url ??
    already_in_xml = len(webpages.findall("./webpage[@domain='" + producer["url"] + "']")) > 0

    ensure_unique_name(producer)    
    if not extractor.contains_producer_with_url(url):
        add_to_database(producer)
    add_to_xml(producer, already_in_xml)
    return producer
    
    
    def ensure_unique_name(producer):
        if producer["name"]=="" or extractor.contains_producer_with_name(producer["name"]):
            producer["name"] = producer["url"]
    
    def add_to_xml(producer, already_in_xml):
        webpage = None
        if already_in_xml:   # Get element and remove existing url-links
            webpage = webpages.find("webpage[@domain='"+producer["url"]+"']")
            webpage.remove(webpage.find("rss-urls"))
        else:  # Create new element
            webpage = ET.Element("webpage", attrib={'domain':producer["url"], 'name':name})
        rss_urls_tag = ET.Element("rss-urls")
        
        for rss_url in rss_urls:  # Add all urls to rss-urls element
            rss = ET.Element("rss")
            rss.text = rss_url
            rss_urls_tag.append(rss)
        webpage.append(rss_urls_tag)  # Append rss-urls to webpage element
        if not already_in_xml:
            webpages.append(webpage)
        tree.write(xml_file)
        
        
    def add_to_database(producer):
        new_producer = producer.Producer(
            name = name,
            description = description,
            url = url,
            infos = [],
            source_ratings = [],
            info_ratings = [],
            type_of = "Newspaper")
        new_producer.save()


