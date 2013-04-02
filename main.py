from veracitor.web import runserver
from veracitor.web import crawler
import veracitor.crawler.crawlInterface as ci


def init_crawler():
    ci.set_callback(crawler.crawl_callback)

if __name__ == "__main__":
    init_crawler()
    runserver(ci)
