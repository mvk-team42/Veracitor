# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Compose

class ArticleItem(Item):
    title = Field()
    author = Field()
    date = Field()
    summary = Field()
    
    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __unicode__(self):
        fields = ["title", "author", "date", "summary"]
        for field in fields:
            if not field in self:
                # Needed when debugging tries to print item before all fields are set
                return ""            
        return (self["title"] + " (" + self["author"] + ", " + self["date"] + ")\nSUMMARY: " + self["summary"])



class ArticleLoader(XPathItemLoader):
    default_output_processor = TakeFirst()
    
