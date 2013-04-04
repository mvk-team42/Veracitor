import veracitor.tasks.crawler as crawler
import unittest

class ScrapeTest(unittest.TestCase):
    """Tests the crawler tasks with celery.
    """
    
    def test_scrape_article(self):
        """
        """
        
        res = crawler.scrape_article.delay("http://www.dn.se/nyheter/varlden/nordkoreaexpert-varre-an-pa-mycket-lange")
        
        
            


