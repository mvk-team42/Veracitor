# -*- coding: utf-8 -*-
""" 
.. module:: rssSpider
    :synopsis: This spider is used to scrape an rss-feed that belongs to some specific newspaper, and send all found article items to the pipeline for further processing.

.. moduleauthor:: Gustaf Lindstedt <glindste@kth.se>
.. moduleauthor:: Jonathan Murray <jmu@kth.se>
"""


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
from .utils import *


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
		scrape_rss(response)

            
            
        
        
        
        
        
        
