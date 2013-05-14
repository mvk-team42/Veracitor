# -*- coding: utf-8 -*-
""" 
.. module:: metaNewspaperSpider
    :synopsis: This spider is used to scrape a newspaper website for data about the newspaper and then send it to the pipeline for further processing. Is typically used on newspapers that haven't yet been added.

    .. moduleauthor:: Gustaf Lindstedt <glindste@kth.se>
    .. moduleauthor:: Jonathan Murray <jmu@kth.se>
"""

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
from ....database import *
from .utils import *


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
        return scrape_meta(response)
