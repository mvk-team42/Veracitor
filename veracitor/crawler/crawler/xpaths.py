#!/usr/bin/env python2.7

import xml.etree.ElementTree as ET

class Xpaths:

    def __init__(self, filepath):
        tree = ET.parse(filepath)
        self.root = tree.getroot()
        
    def get_article_xpaths(self, field_name, domain):
        xpaths = self.root.findall("webpage[@domain='"+domain+"']/article-data/"+field_name+"/xpath")
        if len(xpaths) == 0:
            xpaths = self.root.findall("default/article-data/"+field_name+"/xpath") 
        return [xpath.text for xpath in xpaths]

    def get_article_qualification_xpaths(self, domain):
        xpaths = self.root.findall("webpage[@domain='"+domain+"']/article-qualification/xpath")
        if len(xpaths) == 0:
            xpaths = self.root.findall("default/article-qualification/xpath")   
        return [xpath.text for xpath in xpaths]
        
    def get_article_deny_urls(self, domain):
        patterns = self.root.findall("webpage[@domain='"+domain+"']/article-deny-url/pattern")
        if len(patterns) == 0:
            patterns = self.root.findall("default/article-deny-url/pattern")
        return [pattern.text for pattern in patterns]
        
        
    def get_datetime_formats(self, domain):
        formats = self.root.findall("webpage[@domain='"+domain+"']/datetime-formats/format")
        if len(formats) == 0:
            formats = self.root.findall("default/datetime-formats/format")
        return [f.text for f in formats]
        
        
        
    def get_webpage_xpaths(self, field_name, domain):
        xpaths = self.root.findall("webpage[@domain='"+domain+"']/webpage-data/"+field_name+"/xpath")
        if len(xpaths) == 0:
            xpaths = self.root.findall("default/webpage-data/"+field_name+"/xpath") 
        return [xpath.text for xpath in xpaths]
        
