

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawler.xpaths import Xpaths
from crawler.items import ArticleItem



class ArticleSpider(BaseSpider):
    name = "article"
    allowed_domains = ["dn.se"]

    def __init__(self, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)

        self.start_urls = kwargs.get('start_urls').split(',')
        print self.start_urls

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        xpaths = Xpaths('crawler/webpages.xml')
        article = ArticleItem()
        
        for xpath in xpaths.get_title_xpaths("dn.se"):
            article["title"] = hxs.select(xpath).extract()
            break
        
        for xpath in xpaths.get_author_xpaths("dn.se"):
            article["author"] = hxs.select(xpath).extract()
            break
            
        for xpath in xpaths.get_date_xpaths("dn.se"):
            article["date"] = hxs.select(xpath).extract()
            break
            
        for xpath in xpaths.get_summary_xpaths("dn.se"):
            article["summary"] = hxs.select(xpath).extract()
            break
            
        return article
        
