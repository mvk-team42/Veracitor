from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Compose, Join

"""

The data crawled from the web is stored as objects of these Item-classes before being put into the database.
Items can be created entirely manually from outside this module, or using an "Item-loader"

"""

class ArticleItem(Item):
    """
    Crawler-item representing a newspaper article.
    Corresponds to "Information" in database.
    """
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
            return "safe_string_unknown"


class ArticleLoader(XPathItemLoader):
    """
    Used for easier construction of ArticleItem
    """
    default_output_processor = TakeFirst()
    time_published_out = Join()
    summary_out = Join()
    title_out = Join()
    
    
class ProducerItem(Item):
    """
    Crawler-item representing a producer(newspaper).
    Corresponds to "Producer" in database.
    """
    name = Field()
    description = Field()
    url = Field()
    infos = Field()
    source_ratings = Field()
    info_ratings = Field()
    type_of = Field()
    rss_urls = Field()

    
    
    
    
    
    
    
    
    
    
    
