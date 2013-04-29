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
        """
            is called after an item is returned from some spider.
            Different things happen depending on the spider.
        """
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
        """
            Add database object corresponding to the item
        """
        #log.msg("add_to_database")
        if extractor.contains_information(item["url"]):
            log.msg(item["url"] + " already in database")
            return #already in database
        log.msg("extractor returns " + str(extractor.contains_information(item["url"])))
        log.msg(item["url"] + " is new, adding to database")
            
        #utgår från att item["tags"] är en sträng med space-separerade tags, t.ex. "bombs kidnapping cooking"
        tag_strings = re.sub("[^\w]", " ",  item["tags"]).split()
        tags = [extractor.get_tag_create_if_needed(tag_str) for tag_str in tag_strings]
        
        #utgår från att item["publishers"] är en sträng med space-separerade publishers, t.ex. "DN SVD NYT"
        publisher_strings = re.sub("[^\w]", " ",  item["publishers"]).split()
        publishers = [extractor.get_producer_create_if_needed(pub_str, "newspaper") for pub_str in tag_strings]
        
        info = information.Information(
                            title = item["title"],
                            summary = item["summary"],
                            url = item["url"],
                            time_published = self.parse_datetime(item),
                            tags = tags,
                            publishers = publishers,
                            references = [],
                       )
        info.save()       
                                                     
        
    def print_if_unknown(self, article):
        for field in ArticleItem.fields.iterkeys():
            if article[field] == "unknown":
                print article.long_string() + "\n"
                break
        
    def fix_fields(self, item):
        """
            Before: the attributes in item are very "raw". Scraped directly from website.
            
            After: the attributes are trimmed, summary is shortened, time_published is converted to
            db-friendly format.
        """
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

        #replace swedish months with english
        months_in_swedish = {"januari":"january",
            "februari":"february",
            "mars":"march",
            "april":"april",
            "maj":"may",
            "juni":"june",
            "juli":"july",
            "augusti":"august",
            "september":"september",
            "oktober":"october",
            "november":"november",
            "december":"december"}
        for swedish, english in months_in_swedish.items():
            item['time_published'] = item['time_published'].replace(swedish, english)

        updated_keywords = ["uppdaterad: "]
        for word in updated_keywords:
            if word in item["time_published"]:
                item["time_published"] = item["time_published"].split(word)[1]

    # Parse the date from item['time_published'] either using one of the default common formats or a format specified in webpageXpaths.xml
    def parse_datetime(self, item):
        current_dir = dirname(realpath(__file__))
        xpaths = Xpaths(current_dir + '/webpageXpaths.xml')
        domain = urlparse(item['url'])[1]
        datetime_formats = xpaths.get_datetime_formats(domain)
        time = None
        
#        log.msg("first time format: " + str(datetime_formats[0]))
        for time_format in datetime_formats:
            try:
                time = strptime(item['time_published'],time_format)
                break
            except ValueError:
                log.msg("could not parse date using " + time_format)
                
                
                
                """
        if len(datetime_format) > 0:
            log.msg("found time format: " + str(datetime_format[0]))
            time = strptime(item['time_published'],datetime_format[0])
        else:
            log.msg("no time format found, trying defaults on: " + item['time_published'])
            formats = ["%Y-%m-%d %H:%M","%d %B %Y kl %H:%M"]
            for time_format in formats:
                try:
                    time = strptime(item['time_published'],time_format)
                    break
                except ValueError:
                    log.msg("could not parse date using " + time_format)
                """


        if time==None:
            log.msg("time could not be extracted")
            extracted_time = None
        else:
            log.msg("time extracted: Year=" + str(time.tm_year) + " Month=" + str(time.tm_mon) + " Day=" + str(time.tm_mday) + " Hour=" + str(time.tm_hour) + " Min=" + str(time.tm_min))
            extracted_time = datetime.fromtimestamp(mktime(time))

        return extracted_time
            
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
