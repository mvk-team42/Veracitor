import veracitor.crawler.crawlInterface as ci

#run tests

#ci.addNewspaper("www.svd.se")


ci.set_callbacks(a,b)
ci.requestScrape("www.dn.se")

def a(item, id):
    print "   id: " + str(id)
    print item.values()
    
def b(item, id):
    print "   id: " + str(id)
    print item.values()
