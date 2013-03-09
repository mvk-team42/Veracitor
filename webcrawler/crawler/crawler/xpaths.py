#!/usr/bin/env python2.7

import xml.etree.ElementTree as ET

class Xpaths:

    def __init__(self, filepath):
        tree = ET.parse(filepath)
        self.root = tree.getroot()
        
    def get_xpaths(self, field_name, domain):
        webpage = self.root.find("webpage[@domain='"+domain+"']")
        xpaths = webpage.findall("article-data/"+field_name+"/xpath")
        return [xpath.text for xpath in xpaths]

    def get_article_qualification_xpaths(self, domain):
        webpage = self.root.find("webpage[@domain='"+domain+"']")
        if webpage is None: # Doesn't even recognise domain =>  Certainly not valid article
            return []
        xpaths = webpage.findall("article-qualification/xpath")
        return [xpath.text for xpath in xpaths]
