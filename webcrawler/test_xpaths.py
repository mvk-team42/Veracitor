#!/usr/bin/env python2.7

import xpaths

# initialize object
x = xpaths.Xpaths('webpages.xml')

#test title
x.get_title('dn.se')
