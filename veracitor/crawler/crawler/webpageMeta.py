# -*- coding: utf-8 -*-

""" 
.. module:: webpageMeta
    :synopsis: The interface for the webpageMeta.xml file.

    .. moduleauthor:: Gustaf Lindstedt <glindste@kth.se>
    .. moduleauthor:: Jonathan Murray <jmu@kth.se>
"""


import xml.etree.ElementTree as ET

class WebpageMeta:
    """
        Provides access to an XML-file containing xpaths and general info about known webpages. For instance xpaths to different article-attributes
        such as title, author, summary...
    """

    def __init__(self, filepath):
        tree = ET.parse(filepath)
        self.root = tree.getroot()

    def get_all_webpage_domains(self):
        return self.root.findall("webpage/@domain")
        
    def get_article_xpaths(self, field_name, domain):
        """
            Get an array of xpath-strings that describe the webpage location of given field (for instance author, title ...)
           
            Not to be confused with get_webpage_xpaths. That one is about the start page. This is about article pages.

            Args:
                *field_name*: Name of the field to be accessed.
                *domain*: The domain url. Should be a base url of the webpage (with http://) such as http://www.guardian.co.uk or http://www.dn.se ... if domain is not found in file, default value will be used.

            Returns:
                A list containing extracted xpath strings.
        """
        xpaths = self.root.findall("webpage[@domain='"+domain+"']/article-paths/"+field_name+"/xpath")
        if len(xpaths) == 0:
            xpaths = self.root.findall("default/article-paths/"+field_name+"/xpath") 
        return [xpath.text for xpath in xpaths]

    def get_article_deny_urls(self, domain):
        """
            Get an array of url-strings that if contained in a url, stops spiders, that are looking for articles, from visiting it.

            Args:
                *domain*: The domain url. Should be a base url of the webpage (with http://) such as http://www.guardian.co.uk or http://www.dn.se ... if domain is not found in file, default value will be used.

            Returns:
                A list containing deny-strings for this domain.
        """
        patterns = self.root.findall("webpage[@domain='"+domain+"']/article-deny-url/pattern")
        if len(patterns) == 0:
            patterns = self.root.findall("default/article-deny-url/pattern")
        return [pattern.text for pattern in patterns]
        
        
    def get_datetime_formats(self, domain):
        """
            Get an array of format-strings that describe how timestamps on given domain should be parsed.
            
            Args:
                *domain*: The domain url. Should be a base url of the webpage (with http://) such as http://www.guardian.co.uk or http://www.dn.se ... if domain is not found in file, default value will be used.

            Returns:
                None
        """
        formats = self.root.findall("webpage[@domain='"+domain+"']/datetime-formats/format")
        if len(formats) == 0:
            formats = self.root.findall("default/datetime-formats/format")
        return [f.text for f in formats]
        
        
    def get_webpage_xpaths(self, field_name, domain):
        """
            Get an array of xpath-strings that describe the webpage location of given field (for instance name, description, rss-link...)
            
            Not to be confused with get_article_xpaths. That one is about articles. This is about the start page.
            
            Args:
                *field_name*: The name of the vield to be accessed.
                *domain*: The domain url. Should be a base url of the webpage (with http://) such as http://www.guardian.co.uk or http://www.dn.se ... if domain is not found in file, default value will be used.

            Returns:
                A list containing extracted xpath-strings.
        """
        xpaths = self.root.findall("webpage[@domain='"+domain+"']/webpage-paths/"+field_name+"/xpath")
        if len(xpaths) == 0:
            xpaths = self.root.findall("default/webpage-paths/"+field_name+"/xpath") 
        return [xpath.text for xpath in xpaths]

    def get_rss_urls(self, domain):
        """
            Get an array of the rss-urls associated with the given domain.

            Args:
                *domain*: The domain url. Should be a base url of the webpage (with http://) such as http://www.guardian.co.uk or http://www.dn.se ... if domain is not found in file, default value will be used.

            Returns:
                A list of rss-urls.
        """
        urls = self.root.findall("webpage[@domain='"+domain+"']/rss-urls/url")
        return [url.text for url in urls if url.text != None]
