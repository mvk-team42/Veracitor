# crawler.py
# ===========
# Defines tasks for the crawler.

try:
    from veracitor.tasks.tasks import taskmgr
except:    
    from tasks import taskmgr
    
from ..crawler import crawlInterface as ci


@taskmgr.task
def scrape_article(url):
    ci.scrape_article(url)
    res = "scraped article: " + url
    return res


@taskmgr.task
def add_newspaper(url):
    ci.add_newspaper(url)
    return "added newspaper: " + url

    
@taskmgr.task
def request_scrape(url):
    ci.request_scrape(url)
    return "requested scrape for: " + url
