from celery import task
from ..crawler import crawlerInterface as ci

@task()
def scrape_article(url):
    ci.init_interface()
    ci.scrape_article(url)
