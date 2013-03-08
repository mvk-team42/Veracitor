from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawler.xpaths import Xpaths
<<<<<<< HEAD
from crawler.items import ArticleItem
<<<<<<< HEAD
from urlparse import urlparse

=======
=======
from crawler.items import ArticleItem, ArticleLoader
>>>>>>> Fixed spider-loader bug?
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from items import ArticleItem
>>>>>>> itemloaders in spider


class ArticleSpider(BaseSpider):
    name = "article"
    allowed_domains = ["dn.se"]

    def __init__(self, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls').split(',')

    def parse(self, response):
    
        xpaths = Xpaths('crawler/webpages.xml')
        domain = urlparse(response.url)[1]
        loader = XPathItemLoader(item=ArticleItem(), response=response)
        loader.default_output_processor = TakeFirst()
        
        for xpath in xpaths.get_title_xpaths(domain):
<<<<<<< HEAD
<<<<<<< HEAD
            article["title"] = hxs.select(xpath).extract()
            break
        
        for xpath in xpaths.get_author_xpaths(domain):
            article["author"] = hxs.select(xpath).extract()
            break
            
        for xpath in xpaths.get_date_xpaths(domain):
            article["date"] = hxs.select(xpath).extract()
            break
            
        for xpath in xpaths.get_summary_xpaths(domain):
            article["summary"] = hxs.select(xpath).extract()
            break
=======
=======
>>>>>>> Fixed spider-loader bug?
            loader.add_xpath("name", xpath)
        
        for xpath in xpaths.get_author_xpaths(domain):
            loader.add_xpath("author", xpath)
            
        for xpath in xpaths.get_date_xpaths(domain):
            loader.add_xpath("date", xpath)
<<<<<<< HEAD
            
        for xpath in xpaths.get_summary_xpaths(domain):
            loader.add_xpath("summary", xpath)
>>>>>>> itemloaders in spider
=======
           
        for xpath in xpaths.get_summary_xpaths(domain):
            loader.add_xpath("summary", xpath)
>>>>>>> Fixed spider-loader bug?
            
        return loader.load_item()
        
       
    
    
    
    
        
