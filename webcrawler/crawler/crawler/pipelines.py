from items import ArticleItem
import re

class CrawlerPipeline(object):

    def process_item(self, item, spider):
        self.fix_fields(item)
        print item.long_string() + "\n"
        return item
        
    def fix_fields(self, item):
        self.fix_date(item)
        self.shorten_summary(item)
        for field in ArticleItem.fields.iterkeys():
            self.fix_field(item, field)  
                
    def fix_date(self, item):
        if "date" in item:
            pattern = re.compile(re.escape('published'), re.IGNORECASE)
            item["date"] = pattern.sub("", item["date"])
            swedish_pattern = re.compile(re.escape('publicerad'), re.IGNORECASE)
            item["date"] = swedish_pattern.sub("", item["date"])
            
    def shorten_summary(self, item):
        if "summary" in item:
            item["summary"] = item["summary"][:200]
            
    def fix_field(self, item, field):
            if field in item:
                if item[field].strip() != "":
                    item[field] = item[field].strip().replace("\n", "")
                    return
            item[field] = "unknown"
