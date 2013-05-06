# -*- coding: utf-8 -*-

import re
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import log
from datetime import datetime
from datetime import date
from os.path import dirname, realpath
from urlparse import urlparse
from time import strptime, mktime
import re

from .items import ArticleItem
from .webpageMeta import WebpageMeta
from .spiders.newspaperBankSpider import NewspaperBankSpider
from .spiders.newspaperSpider import NewspaperSpider
from .spiders.metaNewspaperSpider import MetaNewspaperSpider
from .spiders.articleSpider import ArticleSpider
from .spiders.rssSpider import RssSpider
from ...database import *
from ...logger import *
        
def process_article(article, spider):
    fix_fields(article)
    add_to_database(article)
    return article
        
def add_to_database(article):
    """
        Add database object corresponding to the article
    """
    #log.msg("add_to_database")
    if extractor.contains_information(article["url"]):
        log.msg(article["url"] + " already in database")
        return #already in database
    log.msg("extractor returns " + str(extractor.contains_information(article["url"])))
    log.msg(article["url"] + " is new, adding to database")
        
    #utgar fran att article["tags"] är en strang med space-separerade tags, t.ex. "bombs kidnapping cooking"
    tag_strings = re.sub("[^\w]", " ",  article["tags"]).split()
    tags = [extractor.get_tag_create_if_needed(tag_str) for tag_str in tag_strings]

    # lägg till urlen artikeln är på

    #utgår från att article["publishers"] är en sträng med space-separerade publishers, t.ex. "DN SVD NYT"
    publisher_strings = re.sub("[^\w]", " ",  article["publishers"]).split()
    log.msg("pubStrings: " + str(tag_strings))
    publishers = [extractor.producer_create_if_needed(pub_str, "newspaper") for pub_str in publisher_strings]
    
    info = information.Information(
                        title = article["title"],
                        summary = article["summary"],
                        url = article["url"],
                        time_published = parse_datetime(article),
                        tags = tags,
                        publishers = publishers,
                        references = [],
                   )
    info.save()       
    for publisher in publishers:
        log.msg("publisher name: " + publisher.name)
        publisher.infos.append(info)
        publisher.save()
    
def print_if_unknown(article):
    for field in Articlearticle.fields.iterkeys():
        if article[field] == "unknown":
            print article.long_string() + "\n"
            break
    
def fix_fields(article):
    """
        Before: the attributes in article are very "raw". Scraped directly from website.
        
        After: the attributes are trimmed, summary is shortened, time_published is converted to
        db-friendly format.
    """
    fix_time_published(article)
    shorten_summary(article)
    for field in ArticleItem.fields.iterkeys():
        fix_field(article, field)  
            
def fix_time_published(article):
    if "time_published" in article:
        remove_words_from_time_published(article)
        replace_words_in_time_published(article)
                
def remove_words_from_time_published(article):
    pattern = re.compile(re.escape('published'), re.IGNORECASE)
    article["time_published"] = pattern.sub("", article["time_published"])
    swedish_pattern = re.compile(re.escape('publicerad'), re.IGNORECASE)
    article["time_published"] = swedish_pattern.sub("", article["time_published"])
    
def replace_words_in_time_published(article):
    special_words = ["idag", "i dag", "today"]
    pattern = re.compile(re.escape("idag") + "|" + re.escape("i dag") + "|" + re.escape("today") + "|" + re.escape("idag:") + "|" + re.escape("i dag:") + "|" + re.escape("today:"), re.IGNORECASE)
    article["time_published"] = pattern.sub(date.today().isoformat(), article["time_published"])        
    
    #for word in special_words:
    #    article["time_published"] = article["time_published"].replace(word, date.today().isoformat())

    #replace swedish months with english
    months_in_swedish = {"januari":"january",
        "februari":"february",
        "mars":"march",
        "april":"april",
        "maj":"may",
        "juni":"june",
        "juli":"july",
        "augusti":"august",
        "september":"september",
        "oktober":"october",
        "november":"november",
        "december":"december"}
    for swedish, english in months_in_swedish.items():
        article['time_published'] = article['time_published'].replace(swedish, english)

    updated_keywords = ["uppdaterad: "]
    for word in updated_keywords:
        if word in article["time_published"]:
            article["time_published"] = article["time_published"].split(word)[1]

# Parse the date from article['time_published'] either using one of the default common formats or a format specified in webpageXpaths.xml
def parse_datetime(article):
    current_dir = dirname(realpath(__file__))
    meta = WebpageMeta(current_dir + '/webpageMeta.xml')
    domain = urlparse(article['url'])[1]
    datetime_formats = meta.get_datetime_formats(domain)
    time = None
    
#        log.msg("first time format: " + str(datetime_formats[0]))
    for time_format in datetime_formats:
        try:
            time = strptime(article['time_published'],time_format)
            break
        except ValueError:
            log.msg("could not parse date using " + time_format)

    if time==None:
        log.msg("time could not be extracted")
        extracted_time = None
    else:
        log.msg("time extracted: Year=" + str(time.tm_year) + " Month=" + str(time.tm_mon) + " Day=" + str(time.tm_mday) + " Hour=" + str(time.tm_hour) + " Min=" + str(time.tm_min))
        extracted_time = datetime.fromtimestamp(mktime(time))

    return extracted_time
        
def shorten_summary(article):
    if "summary" in article:
        article["summary"] = article["summary"][:200]
        
def fix_field(article, field):
        if field in article:
            if article[field].strip() != "":
                article[field] = article[field].strip().replace("\n", "")
                return
        article[field] = "unknown"
