

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

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        xpaths = Xpaths('crawler/webpages.xml')
        article = ArticleItem()
        
        url = response.url
        domain = urlparse(url)[1]
        
        for xpath in xpaths.get_title_xpaths(domain):
            article["title"] = hxs.select(xpath)[0].extract()
            break
        
        for xpath in xpaths.get_author_xpaths(domain):
            article["author"] = hxs.select(xpath)[0].extract()
            break
            
        for xpath in xpaths.get_date_xpaths(domain):
            article["date"] = hxs.select(xpath)[0].extract()
            break
            
        for xpath in xpaths.get_summary_xpaths(domain):
            article["summary"] = hxs.select(xpath)[0].extract()
            break
            
        return article
        
