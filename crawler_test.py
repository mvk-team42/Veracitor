import veracitor.crawler.crawlInterface as ci
from veracitor.database import *
from veracitor.logger import logger

#run tests

#ci.addNewspaper("www.svd.se")

def a(item, id):
    print "   id: " + str(id)
    print item.values()
    
def b(item, id):
    print "   id: " + str(id)
    print item.values()

logger.log("testing",logger.Level.debug,logger.Area.crawler)

ci.set_callbacks(a,b)
#ci.scrapeArticle("http://www.dn.se/nyheter/varlden/nordkoreaexpert-varre-an-pa-mycket-lange", "1")
ci.scrapeArticle("http://www.svd.se/nyheter/inrikes/utbrett-fiskfusk-avslojat_8046058.svd", "1")



'''
information = information.Information(
                    title = "test",
                    summary = "test",
                    url = "test",
                    time_published = None,
                    tags = [],
                    publishers = [],
                    references = [],
               )
information.save()
'''
