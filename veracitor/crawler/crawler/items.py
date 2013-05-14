# -*- coding: utf-8 -*-

""" 
.. module:: items
    :synopsis: The definitions of items scraped by the crawler.

    .. moduleauthor:: Gustaf Lindstedt <glindste@kth.se>
    .. moduleauthor:: Jonathan Murray <jmu@kth.se>
"""

from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Compose, MapCompose, Join, Identity
from scrapy import log

"""

The data crawled from the web is stored as objects of these Item-classes before being put into the database.
Items can be created entirely manually from outside this module, or using an "Item-loader"

"""

class ArticleItem(Item):
    """
    Crawler-item representing a newspaper article.
    Corresponds to "Information" in database.
    """
    title = Field()           # String
    summary = Field()         # String
    publishers = Field()      # [String]
    time_published = Field()  # [String]
    url = Field()             # String
    tags = Field()            # [String]
    references = Field()      # [String]
    
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
    def is_string(string):
        if isinstance(string, str) or isinstance(string, unicode):
            if string.strip() != "":
                log.msg("returning string: "+ unicode(string.strip()))
                return string.strip()
        log.msg("returning None for string: "+ unicode(string))
        return None

    def separate_tags(tags_string):
        return tags_string.replace(";",",").split(",")

    default_input_processor = MapCompose(is_string)
    default_output_processor = TakeFirst()

    publishers_in = MapCompose(is_string)
    publishers_out = Identity()

    title_in = MapCompose(is_string, unicode.title)
    title_out = TakeFirst()
    
    time_published_in = MapCompose(is_string)
    time_published_out = Identity()

    summary_in = MapCompose(is_string)
    summary_out = TakeFirst()

    tags_in = MapCompose(is_string, separate_tags)
    tags_out = TakeFirst()

    
class ProducerItem(Item):
    """
    Crawler-item representing a producer(newspaper).
    Corresponds to "Producer" in database.
    """
    name = Field()            # String
    description = Field()     # String
    url = Field()             # String
    rss_urls = Field()        # [String]
    type_of = Field()         # String
