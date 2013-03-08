# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader, XPathItemLoader

class ArticleItem(Item):
    title = Field(default="Unknown")
    author = Field(default="Unknown")
    date = Field(default="Unknown")
    summary = Field(default="Unknown")


class ArticleLoader(XPathItemLoader):
    default_output_processor = TakeFirst()
