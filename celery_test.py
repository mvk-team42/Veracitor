import veracitor.tasks.crawler as crawler
import unittest

#class ScrapeTest(unittest.TestCase):
res = None

def t1():
    res = crawler.scrape_article.delay("http://www.dn.se/nyheter/varlden/nordkoreaexpert-varre-an-pa-mycket-lange")


