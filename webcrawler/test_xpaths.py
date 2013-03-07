#!/usr/bin/env python2.7

from xpaths import Xpaths
from pprint import pprint

xpaths = Xpaths('webpages.xml')
url = "dn.se"
pprint(xpaths.get_title(url))
pprint(xpaths.get_summary(url))
pprint(xpaths.get_author(url))
pprint(xpaths.get_date(url))
