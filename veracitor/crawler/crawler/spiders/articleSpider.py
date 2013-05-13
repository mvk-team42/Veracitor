from scrapy.spider import BaseSpider
from scrapy import log

from .utils import *




class ArticleSpider(BaseSpider):

    """
        Crawls a number of articles. (Mostly just one)
        
        The article-urls are given as kwargs in __init__
    """

    name = "article"

    def __init__(self, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]

    def parse(self, response):
        if is_article(response):
            return scrape_article(response)
