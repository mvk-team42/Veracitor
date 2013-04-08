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
    ci.init_interface()
    ci.scrape_article(url)
    return "scraped article: " + url


@taskmgr.task
def add_newspaper(url):
    ci.init_interface()
    ci.add_newspaper(url)
    return "added newspaper: " + url

@taskmgr.task
def request_scrape(url):
    ci.init_interface()
    ci.request_scrape(url)
    return "requested scrape for: " + url
