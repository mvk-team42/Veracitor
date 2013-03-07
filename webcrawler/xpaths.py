#!/usr/bin/env python2.7

import xml.etree.ElementTree as ET

class Xpaths:

    def __init__(self, filepath):
        tree = ET.parse(filepath)
        self.root = tree.getroot()
        
    def _xpaths(self, data):
        webpage = self.root.find("webpage[@url='"+url+"']")
        xpaths = webpage.findall("article-data/"+data+"/xpath")
        return [xpath.text for xpath in xpaths]

    def get_title_xpaths(self, url):
        return _xpaths("title")
        
    def get_summary_xpaths(self, url):
        return _xpaths("summary")

    def get_author_xpaths(self, url):
        return _xpaths("author")

    def get_date_xpaths(self, url):
        return _xpaths("date")
        

