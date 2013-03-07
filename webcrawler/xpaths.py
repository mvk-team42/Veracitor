#!/usr/bin/env python2.7

import xml.etree.ElementTree as ET

class Xpaths:

    def __init__(self, filepath):
        tree = ET.parse(filepath)
        print tree
        self.root = tree.getroot()
        print self.root

    def get_title(self, url):
        path = "./webpage[@url='" + url + "']"
        print path
        print self.root.findall(path)

    def get_author(self, url):
        path = "//"

    def get_date(self, url):
        path = "//"

    def get_text(self, url):
        path = "//"
