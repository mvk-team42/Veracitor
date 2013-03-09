#!/usr/bin/env python2.7

import xml.etree.ElementTree as ET

class Xpaths:

    def __init__(self, filepath):
        tree = ET.parse(filepath)
        self.root = tree.getroot()
        
    def get_xpaths(self, field_name, domain):
        xpaths = self.root.findall("webpage[@domain='"+domain+"']/article-data/"+field_name+"/xpath")

        # No xpath for that field in that domain
        # Luckily there are fallback xpaths for each field
        if len(xpaths) == 0:
            xpaths = self.root.findall("default/article-data/"+field_name+"/xpath")
            
        return [xpath.text for xpath in xpaths]

    def get_article_qualification_xpaths(self, domain):
        xpaths = self.root.findall("webpage[@domain='"+domain+"']/article-qualification/xpath")
        
        if len(xpaths) == 0:
            xpaths = self.root.findall("default/article-qualification/xpath")
            
        return [xpath.text for xpath in xpaths]
