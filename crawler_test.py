import veracitor.crawler.crawlInterface as ci
from veracitor.database import *
from veracitor.logger import logger

#run tests

networkModel.build_network_from_db()

#print "string is " + str(information.Information.objects(url='http://www.dn.se/sport/ishockey/detroit-tillbaka-pa-slutspelsplats-1'))

def a(item, id):
    print "   id: " + str(id)
    print item.values()


#logger.log("testing",logger.Level.debug,logger.Area.crawler)

#ci.set_callback(a)
ci.init_interface()
#ci.add_newspaper("www.svd.se")
#ci.test_rss("http://penguin-news.com/index.php?format=feed&type=rss")
#ci.start_continuous_scrape()
#ci.create_newspaper_bank()
#ci.add_newspaper("www.penguin-news.com")
ci.scrape_article("http://www.dn.se/nyheter/varlden/nordkoreaexpert-varre-an-pa-mycket-lange")
#ci.scrape_article("http://www.svd.se/nyheter/inrikes/utbrett-fiskfusk-avslojat_8046058.svd")
#ci.request_scrape("www.penguin-news.com")
#ci.create_newspaper_bank()




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
