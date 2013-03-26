from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Compose, Join

class ArticleItem(Item):
    title = Field()
    summary = Field()
    publishers = Field()
    time_published = Field()
    url = Field()
    tags = Field()
    regerences = Field()
    
    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __unicode__(self):           
        return (self.safe_str("title") + " (" + self.safe_str("publishers") + ", " + self.safe_str("time_published") + ")\nURL: " + self.safe_str("url") + "\nSUMMARY: " + self.safe_str("summary"))
        
    def long_string(self):
        return ("---------------------------------\n"+
                self.__unicode__() +
                "\n---------------------------------"
               );

    def short_string(self):
        return self["title"]
        
       
    def safe_str(self, field):
        if field in self:
            return unicode(self[field])
        else:
            return "unknown"


class ArticleLoader(XPathItemLoader):
    default_output_processor = TakeFirst()
    date_out = Join()
    summary_out = Join()
    title_out = Join()
