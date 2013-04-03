from veracitor.web import runserver
from veracitor.web import callback
import veracitor.crawler.crawlInterface as ci


def init_crawler():
    pass
    # TODO
    #ci.set_callback(crawler.crawl_callback)

if __name__ == "__main__":
    init_crawler()
    runserver(ci)
