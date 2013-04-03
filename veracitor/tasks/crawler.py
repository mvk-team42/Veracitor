try:
    from veracitor.tasks.tasks import app
except:    
    from tasks import app
    
from ..crawler import crawlInterface as ci

print app

@app.task
def scrape_article(url):
    ci.init_interface()
    ci.scrape_article(url)
    return "added article: " + url


@app.task
def add_newspaper(url):
    ci.init_interface()
    ci.add_newspaper(url)
    return

@app.task
def request_scrape(url):
    ci.init_interface()
    ci.request_scrape(url)
    return
