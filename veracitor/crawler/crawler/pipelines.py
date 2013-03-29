import re
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import log
from datetime import datetime
from datetime import date
from os.path import dirname, realpath
from urlparse import urlparse

from .items import ArticleItem
from .xpaths import Xpaths
from .spiders.newspaperBankSpider import NewspaperBankSpider
from .spiders.newspaperSpider import NewspaperSpider
from .spiders.metaNewspaperSpider import MetaNewspaperSpider
from .spiders.articleSpider import ArticleSpider
from .spiders.rssSpider import RssSpider
from ...database import *
from ...logger import *

class CrawlerPipeline(object):

    def __init__(self):
        self.articles = []
        #dispatcher.connect(self.print_info, signals.spider_closed)

    def process_item(self, item, spider):
    
        if isinstance(spider, NewspaperBankSpider):
            return item
    
    
        self.fix_fields(item)
        #self.print_if_unknown(item)
        self.articles.append(item)
        print item
        print "---------------------"
        self.add_to_database(item)
        return item
        
    def add_to_database(self, item):
        log.msg("add_to_database")
        if extractor.contains_information(item["title"]):
            pass #return #already in database
        info = information.Information(
                            title = item["title"],
                            summary = item["summary"],
                            url = item["url"],
                            time_published = self.parse_datetime(item),
                            tags = [],
                            publishers = [], #item["publishers"],
                            references = [],
                       )
        info.save()       
                                                     
        
    def print_if_unknown(self, article):
        for field in ArticleItem.fields.iterkeys():
            if article[field] == "unknown":
                print article.long_string() + "\n"
                break
        
    def fix_fields(self, item):
        self.fix_time_published(item)
        self.shorten_summary(item)
        for field in ArticleItem.fields.iterkeys():
            self.fix_field(item, field)  
                
    def fix_time_published(self, item):
        if "time_published" in item:
            self.remove_words_from_time_published(item)
            self.replace_words_in_time_published(item)
                    
    def remove_words_from_time_published(self, item):
        pattern = re.compile(re.escape('published'), re.IGNORECASE)
        item["time_published"] = pattern.sub("", item["time_published"])
        swedish_pattern = re.compile(re.escape('publicerad'), re.IGNORECASE)
        item["time_published"] = swedish_pattern.sub("", item["time_published"])
        
    def replace_words_in_time_published(self, item):
        special_words = ["idag", "i dag", "today"]
        for word in special_words:
            item["time_published"] = item["time_published"].replace(word, date.today().isoformat())

    def parse_datetime(self, item):
        current_dir = dirname(realpath(__file__))
        xpaths = Xpaths(current_dir + '/webpageXpaths.xml')
        datetime_format = xpaths.get_xpaths("datetime_format", urlparse(item['url'])[1])
        if len(datetime_format) > 0:
            log.msg("found time format:" + str(datetime_format))
        return None
            
    def shorten_summary(self, item):
        if "summary" in item:
            item["summary"] = item["summary"][:200]
            
    def fix_field(self, item, field):
            if field in item:
                if item[field].strip() != "":
                    item[field] = item[field].strip().replace("\n", "")
                    return
            item[field] = "unknown"
            
            
    def print_info(self, spider):
        print "Number of articles: " + str(len(self.articles))
        unknowns = self.count_unknowns()
        for field in unknowns:
            print "Number of unknown " + field + ": " + str(unknowns[field])
        
    def count_unknowns(self):
        unknowns = {}
        for field in ArticleItem.fields.iterkeys():
            unknowns[field] = 0
            for article in self.articles:
                if article[field] == "unknown":
                    unknowns[field] += 1
        return unknowns
