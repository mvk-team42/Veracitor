from items import ArticleItem
import re
from datetime import date
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class CrawlerPipeline(object):

    def __init__(self):
        self.articles = []
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):
        self.fix_fields(item)
        self.print_if_unknown(item)
        self.articles.append(item)
        return item
        
    def print_if_unknown(self, article):
        for field in ArticleItem.fields.iterkeys():
            if article[field] == "unknown":
                print article.long_string() + "\n"
                break
        
    def fix_fields(self, item):
        self.fix_date(item)
        self.shorten_summary(item)
        for field in ArticleItem.fields.iterkeys():
            self.fix_field(item, field)  
                
    def fix_date(self, item):
        if "date" in item:
            self.remove_words_from_date(item)
            self.replace_words_in_date(item)
                    
    def remove_words_from_date(self, item):
        pattern = re.compile(re.escape('published'), re.IGNORECASE)
        item["date"] = pattern.sub("", item["date"])
        swedish_pattern = re.compile(re.escape('publicerad'), re.IGNORECASE)
        item["date"] = swedish_pattern.sub("", item["date"])
        
    def replace_words_in_date(self, item):
        special_words = ["idag", "i dag", "today"]
        for word in special_words:
            item["date"] = item["date"].replace(word, date.today().isoformat())
            
    def shorten_summary(self, item):
        if "summary" in item:
            item["summary"] = item["summary"][:200]
            
    def fix_field(self, item, field):
            if field in item:
                if item[field].strip() != "":
                    item[field] = item[field].strip().replace("\n", "")
                    return
            item[field] = "unknown"
            
            
    def spider_closed(self, spider):
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
