# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class CrawlerPipeline(object):
    def process_item(self, item, spider):
    
        fields = ["title", "author", "summary", "date"]
        for field in fields:
            if field in item:
                item[field] = item[field].strip()
            else:
                item[field] = "unknown"
        
        print "ARTICLE:"
        print "-------"
        print item
        print ""
        
        return item
