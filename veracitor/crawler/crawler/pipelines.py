# -*- coding: utf-8 -*-

""" 
.. module:: pipelines
    :synopsis: The wrapper pipeline for the items returned by the crawler. Separates them to their specific pipelines.

.. moduleauthor:: Gustaf Lindstedt <glindste@kth.se>
.. moduleauthor:: Jonathan Murray <jmu@kth.se>
"""

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

from .items import ArticleItem, ProducerItem
from .webpageMeta import WebpageMeta
from .spiders.newspaperBankSpider import NewspaperBankSpider
from .spiders.newspaperSpider import NewspaperSpider
from .spiders.metaNewspaperSpider import MetaNewspaperSpider
from .spiders.articleSpider import ArticleSpider
from .spiders.rssSpider import RssSpider
from ...database import *
from ...logger import *
from .articlePipeline import *
from .producerPipeline import *

class CrawlerPipeline(object):

    def __init__(self):
        self.articles = []
        #dispatcher.connect(self.print_info, signals.spider_closed)

    def process_item(self, item, spider): 
        """
            is called after an item is returned from some spider.
            Different things happen depending on the spider.
        """
        if isinstance(item, ArticleItem):
            return process_article(item, spider)
        if isinstance(item, ProducerItem):
            return process_producer(item, spider)
        raise Exception("Item type not recognized!")
