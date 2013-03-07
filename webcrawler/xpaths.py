#!/bin/python2.7

import xml.etree.ElementTree as ET

class Xpaths:

    def __init__(self, filepath):
        tree = ET.parse(filepath)
        self.root = tree.getroot()

    def get_title(self, url):

    def get_author(self, url):

    def get_date(self, url):

    def get_text(self, url):

