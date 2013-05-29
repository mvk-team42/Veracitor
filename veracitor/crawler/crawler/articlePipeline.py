# -*- coding: utf-8 -*-

""" 
.. module:: articlePipeline
    :synopsis: The pipeline for articleItems scraped by the crawler. The items are cleaned, filtered and added to the database. Some additional work is done, such as setting trust ratings between the producers of the same article.

.. moduleauthor:: Gustaf Lindstedt <glindste@kth.se>
.. moduleauthor:: Jonathan Murray <jmu@kth.se>
"""

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
    """
        Processes the article item and adds it to the database.
        Makes the relevant connections between article and producers.

        Args:
            *article*: An ArticleItem.

            *spider*: The spider which screaped the item.

        Returns:
            An ArticleItem.
    """
    #log.msg("tags type: "+unicode(type(article["tags"]))+" tags: "+unicode(article["tags"]))

    # FULHACK
    if "publishers" in article:
        article["publishers"] = article["publishers"][:1]
        
    _fix_fields(article)
    article["time_published"] = _parse_datetime(article)
    _add_to_database(article)
    return article
        
def _add_to_database(article):
    """
        Add database object corresponding to the article
    """
    #log.msg("add_to_database")
    if extractor.contains_information(article["url"]):
        #log.msg(article["url"] + " already in database")
        return #already in database
    #log.msg("extractor returns " + str(extractor.contains_information(article["url"])))
    #log.msg(article["url"] + " is new, adding to database")
        

    article["publishers"] = _get_publisher_objects(article)

    info = information.Information(
                        title = article["title"],
                        summary = article["summary"],
                        url = article["url"],
                        time_published = article["time_published"],
                        tags = article["tags"],
                        publishers = article["publishers"],
                        references = [],
                   )
    info.save()       
    for publisher in article["publishers"]:
        #log.msg("publisher name: " + publisher.name)
        publisher.infos.append(info)
        publisher.rate_information(info, 5)
        
        # Add trust between publishers
        for publisher2 in article["publishers"]:
            if not publisher==publisher2:
                #log.msg("publisher2 name: " + publisher2.name)
                for tag in article["tags"]:
                    publisher.rate_source(publisher2, tag, 5)
        publisher.save()

def _get_publisher_objects(article):
    #publisher_strings = [string.replace(".",",").replace("$",",") for string in publisher_strings]
    publisher_strings = article["publishers"]
    #log.msg("pubStrings: " + str(publisher_strings))
    publishers = []
    for publisher_string in publisher_strings:
        split_publishers = re.sub("[-&;/]", ",", publisher_string).split(",")
        for split_publisher in split_publishers:
            if split_publisher == 'unknown':   #Nödvändig?
                continue
            if extractor.contains_producer_with_name(split_publisher):
                publishers.append(extractor.get_producer(split_publisher))
            else:
                # If not found, split on whitespace and try again
                spaced_publishers = split_publisher.split()
                not_found = []
                for index, spaced_publisher in enumerate(spaced_publishers):
                    if extractor.contains_producer_with_name(spaced_publisher):
                        publishers.append(extractor.get_producer(spaced_publisher))
                    else:
                        not_found.append(spaced_publisher)
                if len(not_found) != 0:
                    producer = extractor.producer_create_if_needed(" ".join(not_found), "Journalist")
                    publishers.append(producer)

    domain = "http://" + urlparse(article["url"])[1]
    try:
        publishers.append(extractor.get_producer_with_url(domain))
        #log.msg("got producer")
    except:
        #log.msg("failed to get producer....")
        pass

    return publishers

    
def print_if_unknown(article):
    for field in Articlearticle.fields.iterkeys():
        if article[field] == "unknown":
            print article.long_string() + "\n"
            break
    
def _fix_fields(article):
    """
        Before: the attributes in article are very "raw". Scraped directly from website.
        
        After: the attributes are trimmed, summary is shortened, time_published is converted to
        db-friendly format.
    """
    _fix_time_published(article)
    _fix_publishers(article)
    _fix_tags(article)
    _fix_references(article)
    _shorten_title(article)
    _shorten_summary(article)
    for field in ArticleItem.fields.iterkeys():
        if field in article:
            if isinstance(article[field], str) or isinstance(article[field], unicode):
                _fix_string_field(article, field)
        else:
            # We know it's a string, since all list fields have been fixed
            article[field] = "unknown"
        
def _fix_string_field(article, field):
    if article[field].strip() != "":
        article[field] = re.sub("\s+", " ", article[field].strip())
        #log.msg("article["+field+"]: "+article[field])
        return
    article[field] = "unknown"
    
def _fix_publishers(article):
    if "publishers" in article:
        _remove_words_from_publishers(article)
        for index in range(len(article["publishers"])):
            article["publishers"][index] = article["publishers"][index].strip()
    else:
        article["publishers"] = []

def _fix_tags(article):

	#Maps predefined tags to words that potentially have the same meaning
    tag_map = {}
    tag_map["Crime"] = ["crime", "assault", "murder", "robber", "safety"]
    tag_map["Crime"] += ["brott", "överfall", "mord", "rån", "säkerhet"]
    tag_map["Culture"] = ["music", "art", "painting", "culture", "concert", "movie", "tv", "radio", "food", "wine", "drink", "beer"]
    tag_map["Culture"] = ["musik", "konst", "målning", "kultur", "koncert", "film", "mat", "vin", "dryck", "öl"]
    tag_map["Politics"] = ["court", "attourney", "jury", "health", "supreme", "reform", "ruling", "politic", "committee", "diplom", "party", "vote", "election"]
    tag_map["Politics"] = ["domstol", "häls", "parti", "komitte", "parti", "röst", "val"]
    tag_map["Sports"] = ["ball", "match", "tournament", "champion", "sport", "win"]
    tag_map["Sports"] = ["boll", "turnering", "mästar", "vinna"]
    tag_map["Finances"] = ["recession", "financ", "money", "bank", "compan", "price"]
    tag_map["Finances"] = ["finans", "penga", "kompan"]
    
    final_tags = []
    
    if "tags" in article:
    	for tag_str in article["tags"]:
            for predefined_tag in tag_map:
                if predefined_tag in final_tags:
                    continue
                # If tag_str matches any of the strings mapped to the predefined tag
                if any(str(match) in str(tag_str) for match in tag_map[predefined_tag]): 
                    final_tags.append(predefined_tag)
        #log.msg("final tags: "+unicode(final_tags))
        final_tags.append("General") # Add the general tag, should always be rated
        article["tags"] = [extractor.get_tag_create_if_needed(tag_str) for tag_str in final_tags]
    else:
        article["tags"] = []
	

def _fix_references(article):
    if "references" in article:
        pass
    else:
        article["references"] = []

def _remove_words_from_publishers(article):
    pattern = re.compile("\S+:|av|by|\sin\s.*|\sin$", re.IGNORECASE)
    for index, publisher_string in enumerate(article["publishers"]):
        article["publishers"][index] = pattern.sub("", publisher_string)

            
def _fix_time_published(article):
    if "time_published" in article:
        _remove_words_from_time_published(article)
        _replace_words_in_time_published(article)
                
def _remove_words_from_time_published(article):
    pattern = re.compile('published:|publicerad:|published|publicerad|am|pm|\son\s|\sden\s', re.IGNORECASE)
    day_pattern = re.compile('monday|tuesday|wednesday|thursday|friday|saturday|sunday|måndag|tisdag|onsdag|torsdag|fredag|lördag|söndag', re.IGNORECASE)
    for index, time_string in enumerate(article["time_published"]):
        article["time_published"][index] = pattern.sub("", time_string)   
        article["time_published"][index] = day_pattern.sub("", time_string)
    
def _replace_words_in_time_published(article):
    special_words = ["idag", "i dag", "today"]
    pattern = re.compile(re.escape("idag") + "|" + re.escape("i dag") + "|" + re.escape("today")
            + "|" + re.escape("idag:") + "|" + re.escape("i dag:") + "|" + re.escape("today:"), re.IGNORECASE)

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
    updated_keywords = ["uppdaterad: "]

    for index, time_string in enumerate(article["time_published"]):
        time_string = pattern.sub(date.today().isoformat(), time_string)        
        for swedish, english in months_in_swedish.items():
            time_string = time_string.replace(swedish, english)
        for word in updated_keywords:
            if word in time_string:
                time_string = time_string.split(word)[1]
        article["time_published"][index] = time_string
    
    #for word in special_words:
    #    article["time_published"] = article["time_published"].replace(word, date.today().isoformat())



# Parse the date from article['time_published'] either using one of the default common formats or a format specified in webpageXpaths.xml
def _parse_datetime(article):
    current_dir = dirname(realpath(__file__))
    meta = WebpageMeta(current_dir + '/webpageMeta.xml')
    domain = urlparse(article['url'])[1]
    datetime_formats = meta.get_datetime_formats(domain)
    
    #log.msg("first time format: " + str(datetime_formats[0]))
    for datetime_string in article["time_published"]:
        #log.msg("time string: "+unicode(datetime_string))
        for time_format in datetime_formats:
            try:
                time = strptime(datetime_string,time_format)
                #log.msg("time extracted: Year=" + str(time.tm_year) + " Month=" + str(time.tm_mon) + " Day=" + str(time.tm_mday) + " Hour=" + str(time.tm_hour) + " Min=" + str(time.tm_min))
                return datetime.fromtimestamp(mktime(time))
            except ValueError:
                #log.msg("could not parse date using " + time_format)
                pass

    #log.msg("time could not be extracted")
    return None

        
def _shorten_summary(article):
    if "summary" in article and len(article["summary"]) > 200:
        article["summary"] = article["summary"][:197] + "..."

def _shorten_title(article):
    if "title" in article and len(article["title"]) > 100:
        article["title"] = article["title"][:97] + "..."
