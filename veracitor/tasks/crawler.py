from celery import task
from ..crawler import crawlInterface as ci

@task()
def scrape_article(url):
    ci.init_interface()
    ci.scrape_article(url)
