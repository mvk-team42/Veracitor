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
import xml.etree.ElementTree as ET

from .items import ArticleItem, ProducerItem
from .webpageMeta import WebpageMeta
from .spiders.newspaperBankSpider import NewspaperBankSpider
from .spiders.newspaperSpider import NewspaperSpider
from .spiders.metaNewspaperSpider import MetaNewspaperSpider
from .spiders.articleSpider import ArticleSpider
from .spiders.rssSpider import RssSpider
from ...database import *
from ...logger import *
        
def process_producer(producer_item, spider):

    current_dir = dirname(realpath(__file__))
    xml_file = current_dir + '/webpageMeta.xml'
    tree = ET.parse(xml_file)
    webpages = tree.getroot()
    # Might wanna httpify all uses of producer.url ??

    fix_fields(producer_item)

    if producer_item["name"]=="unknown":
        producer_item["name"] = producer_item["url"]

    if extractor.contains_producer_with_name(producer_item["name"]):
        existing_producer = extractor.get_producer(producer_item["name"])
        if (existing_producer.url != producer_item["url"] and not extractor.contains_producer_with_name(producer_item["url"])):
            producer_item["name"] = producer_item["url"]
            add_to_database(producer_item)
    else:
        add_to_database(producer_item)

    add_to_xml(producer_item, tree, xml_file)
    return producer_item
    
    
def add_to_xml(producer_item, tree, xml_file):
    webpages = tree.getroot()
    already_in_xml = len(webpages.findall("./webpage[@domain='" + producer_item["url"] + "']")) > 0
    webpage = None

    if already_in_xml:   # Get element and remove existing url-links
        webpage = webpages.find("webpage[@domain='"+producer_item["url"]+"']")
        if webpage.find("rss-urls") != None:
            webpage.remove(webpage.find("rss-urls"))
    else:  # Create new element
        webpage = ET.Element("webpage", attrib={'domain':producer_item["url"], 'name':producer_item["name"]})
    rss_urls_tag = ET.Element("rss-urls")
    
    for rss_url in producer_item["rss_urls"]:  # Add all urls to rss-urls element
        rss = ET.Element("rss")
        rss.text = rss_url
        rss_urls_tag.append(rss)
    webpage.append(rss_urls_tag)  # Append rss-urls to webpage element
    if not already_in_xml:
        webpages.append(webpage)
    tree.write(xml_file)
    
    
def add_to_database(producer_item):
    new_producer = producer.Producer(
        name = producer_item["name"], #.replace(".",",").replace("$",","),
        description = producer_item["description"],
        url = producer_item["url"],
        infos = [],
        source_ratings = {},
        info_ratings = {},
        type_of = "Newspaper")
    new_producer.save()

def fix_fields(producer_item):
    for field in ProducerItem.fields.iterkeys():
        fix_field(producer_item, field)

def fix_field(producer_item, field):
    if field in producer_item:
        log.msg("producer_item["+field+"]: "+unicode(producer_item[field]))
        if isinstance(producer_item[field], unicode) or isinstance(producer_item[field], str):
            if producer_item[field].strip() != "":
                producer_item[field] = re.sub("\s+", " ", producer_item[field].strip())
                return
    #rss_urls is expected to be in list format, when it is sent to pipeline.        
    if field == "rss_urls":
        producer_item[field] = []
    else:
        producer_item[field] = "unknown"
