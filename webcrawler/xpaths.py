#!/usr/bin/env python2.7

import xml.etree.ElementTree as ET

class Xpaths:

    def __init__(self, filepath):
        tree = ET.parse(filepath)
        self.root = tree.getroot()
        
    def _webpage(self, url):
        return self.root.find("webpage[@url='"+url+"']")

    def get_title(self, url):
        webpage = self._webpage(url)
        xpaths = webpage.findall("article-data/title/xpath")
        return [xpath.text for xpath in xpaths]
        
    def get_summary(self, url):
        webpage = self._webpage(url)
        xpaths = webpage.findall("article-data/summary/xpath")
        return [xpath.text for xpath in xpaths]

    def get_author(self, url):
        webpage = self._webpage(url)
        xpaths = webpage.findall("article-data/author/xpath")
        return [xpath.text for xpath in xpaths]

    def get_date(self, url):
        webpage = self._webpage(url)
        xpaths = webpage.findall("article-data/date/xpath")
        return [xpath.text for xpath in xpaths]
        
