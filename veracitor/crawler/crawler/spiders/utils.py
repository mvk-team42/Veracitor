# -*- coding: utf-8 -*-
'''
.. module:: utils
    :synopsis: Utility methods used by spiders.

.. moduleauthor:: Gustaf Lindstedt <glindste@kth.se>
.. moduleauthor:: Jonathan Murray <jmu@kth.se>
'''

from os.path import realpath, dirname
from urlparse import urlparse
import urllib2 

from scrapy.selector import HtmlXPathSelector
from scrapy.http.response.text import *
from scrapy.utils.python import unicode_to_str
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy import log

from ..webpageMeta import WebpageMeta
from ..items import ArticleItem, ArticleLoader, ProducerItem
from ....database import *

current_dir = dirname(realpath(__file__))
meta = WebpageMeta(current_dir + '/../webpageMeta.xml')

def is_article(response):
    """
        Checks if the response body is an article.

        Args:
            *response*: A response object.

        Returns:
            A boolean, True if it is an article and False if it isn't.
    """
    domain = urlparse(response.url)[1]
    hxs = HtmlXPathSelector(response)
    for xpath in meta.get_article_xpaths("qualification",domain):
        if len(hxs.select(xpath)) > 0:
            return True
    return False

def scrape_article(response):
    """
        Scrapes the response as an article.

        Args:
            *response*: A response object.

        Returns:
            A generator that yields scraped items. Could be a ProdcerItem and an ArticleItem, or just an ArticleItem.
    """
    domain = urlparse(response.url)[1]
    loader = ArticleLoader(item=ArticleItem(), response=response)
    
    mainpage_domain = "http://" + urlparse(response.url)[1]
    log.msg("page: "+str(mainpage_domain))
    if not extractor.contains_producer_with_url(mainpage_domain):
        # Construct a response object and send to scrape_meta
        mainpage_body = urllib2.urlopen(mainpage_domain).read()
        mainpage_response = TextResponse(url=mainpage_domain,body=unicode_to_str(mainpage_body, 'utf-8'),encoding='utf-8')
        yield scrape_meta(mainpage_response)
    
    for field in ArticleItem.fields.iterkeys():
        #log.msg("field: " + field)
        for xpath in meta.get_article_xpaths(field, domain):
            log.msg("Xpath for field: "+unicode(field)+" "+unicode(xpath))
            loader.add_xpath(field, xpath)
    loader.add_value("url", response.url)
            
    yield loader.load_item()

def scrape_meta(response):
    """
       Scrapes the response as a producer, gathering meta information.

       Args:
           *response*: A response object.

       Returns:
           A ProducerItem.
    """

    producer_item = ProducerItem()
    hxs = HtmlXPathSelector(response)

    producer_item["name"] = extract_name(response.url, hxs)
    producer_item["rss_urls"] = extract_rss_urls(response.url, hxs)
    producer_item["description"] = extract_description(response.url, hxs)
    producer_item["url"] = response.url
    producer_item["type_of"] = "Newspaper"

    return producer_item
     
     
    
#These three should be in some ItemLoader, whatever    
    
def extract_name(domain, hxs):
    """
       Extracts the producer name using the provided HtmlXPathSelector.

       Args:
           *domain*: The domain url.

           *hxs*: An initialized HtmlXPathSelector.

       Returns:
           A string representing the name.
    """
    for name_xpath in meta.get_webpage_xpaths("name", domain):
        names = hxs.select(name_xpath)
        if len(names) > 0:
            return names[0].extract().strip()
    return ""

def extract_rss_urls(domain, hxs):
    """
       Extracts the rss urls using the provided HtmlXPathSelector.

       Args:
           *domain*: The domain url.

           *hxs*: An initialized HtmlXPathSelector.

       Returns:
           A list containing the found rss urls.
    """
    for rss_xpath in meta.get_webpage_xpaths("rss-link", domain):
        rss_links = hxs.select(rss_xpath)
        if len(rss_links) > 0:
            return [rss_link.extract().strip() for rss_link in rss_links]
    return []

def extract_description(domain, hxs):
    """
       Extracts the description using the provided HtmlXPathSelector.

       Args:
           *domain*: The domain url.

           *hxs*: An initialized HtmlXPathSelector.

       Returns:
           A string with representing the description.
    """
    for description_xpath in meta.get_webpage_xpaths("description", domain):
        descriptions = hxs.select(description_xpath)
        if len(descriptions) > 0:
            return descriptions[0].extract().strip()
    return "No description scraped."
