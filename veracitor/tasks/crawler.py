# crawler.py
# ===========
# Defines tasks for the crawler.

try:
    from veracitor.tasks.tasks import taskmgr
except:    
    from tasks import taskmgr
    
from ..crawler import crawlInterface as ci


@taskmgr.task
def anton():
    import time
    time.delay(400)
    return "Yay!"

@taskmgr.task
def scrape_article(url):
    ci.init_interface()
    err_msg = ""
    try:
        ci.scrape_article(url)
    except ValueError, err:
        err_msg = str(err)

    res = "scraped article: " + url
    if err_msg:
        res += "\nerr: " + err_msg
    return res


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
