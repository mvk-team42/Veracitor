#!/usr/bin/env python2.7

import xml.etree.ElementTree as ET

class Xpaths:
    """
        Provides access to an XML-file containing xpaths and general info about known webpages. For instance xpaths to different article-attributes
        such as title, author, summary...
    """

    def __init__(self, filepath):
        tree = ET.parse(filepath)
        self.root = tree.getroot()
        
    def get_article_xpaths(self, field_name, domain):
        """
            Get an array of xpath-strings that describe the webpage location of given field (for instance author, title ...)
           
            Not to be confused with get_webpage_xpaths. That one is about the start page. This is about article pages.
            
            domain should be a base url of the webpage (without http://) such as www.guardian.co.uk or www.dn.se ... if 
            domain is not found in file, default value will be used.
        """
        xpaths = self.root.findall("webpage[@domain='"+domain+"']/article-data/"+field_name+"/xpath")
        if len(xpaths) == 0:
            xpaths = self.root.findall("default/article-data/"+field_name+"/xpath") 
        return [xpath.text for xpath in xpaths]

    def get_article_qualification_xpaths(self, domain):
        """
            Get an array of xpath-strings that should be found on a webpage for it to be classified as an article.
            
            domain should be a base url of the webpage (without http://) such as www.guardian.co.uk or www.dn.se ... if 
            domain is not found in file, default value will be used.
        """
        xpaths = self.root.findall("webpage[@domain='"+domain+"']/article-qualification/xpath")
        if len(xpaths) == 0:
            xpaths = self.root.findall("default/article-qualification/xpath")   
        return [xpath.text for xpath in xpaths]
        
    def get_article_deny_urls(self, domain):
        """
            Get an array of url-strings that if contained in a url, stops spiders, that are looking for articles, from visiting it.
            
            domain should be a base url of the webpage (without http://) such as www.guardian.co.uk or www.dn.se ... if 
            domain is not found in file, default value will be used.
        """
        patterns = self.root.findall("webpage[@domain='"+domain+"']/article-deny-url/pattern")
        if len(patterns) == 0:
            patterns = self.root.findall("default/article-deny-url/pattern")
        return [pattern.text for pattern in patterns]
        
        
    def get_datetime_formats(self, domain):
        """
            Get an array of format-strings that describe how timestamps on given domain should be parsed.
            
            domain should be a base url of the webpage (without http://) such as www.guardian.co.uk or www.dn.se ... if 
            domain is not found in file, default value will be used.
        """
        formats = self.root.findall("webpage[@domain='"+domain+"']/datetime-formats/format")
        if len(formats) == 0:
            formats = self.root.findall("default/datetime-formats/format")
        return [f.text for f in formats]
        
        
    def get_webpage_xpaths(self, field_name, domain):
        """
            Get an array of xpath-strings that describe the webpage location of given field (for instance name, description, rss-link...)
            
            Not to be confused with get_article_xpaths. That one is about articles. This is about the start page.
            
            domain should be a base url of the webpage (without http://) such as www.guardian.co.uk or www.dn.se ... if 
            domain is not found in file, default value will be used.
        """
        xpaths = self.root.findall("webpage[@domain='"+domain+"']/webpage-data/"+field_name+"/xpath")
        if len(xpaths) == 0:
            xpaths = self.root.findall("default/webpage-data/"+field_name+"/xpath") 
        return [xpath.text for xpath in xpaths]
        
        
        
