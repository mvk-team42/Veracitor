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
    return
