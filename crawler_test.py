import veracitor.crawler.crawlInterface as ci
import veracitor.crawler.gtdParser as gtdp
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
#ci.scrape_article("http://www.dn.se/nyheter/varlden/nordkoreaexpert-varre-an-pa-mycket-lange")
#ci.scrape_article("http://www.svd.se/nyheter/inrikes/mamman-dog-i-vantan-pa-dottern_8152288.svd")
#ci.scrape_article("http://www.guardian.co.uk/uk/2013/may/07/jimmy-tarbuck-arrested-allegation-assault-teenage-boy")
#ci.scrape_article("http://www.svd.se/nyheter/inrikes/utbrett-fiskfusk-avslojat_8046058.svd")
#ci.scrape_article("http://www.dn.se/nyheter/sverige/barn-som-sett-vald-utan-ersattning")
#ci.scrape_article("http://www.nytimes.com/2013/05/10/us/disease-threatens-floridas-citrus-industry.html?hp&_r=0")
#ci.scrape_article("http://www.washingtonpost.com/politics/irs-targeted-groups-critical-of-government-documents-from-agency-probe-show/2013/05/12/bb38e5bc-bb24-11e2-97d4-a479289a31f9_story.html")
#ci.scrape_article("http://www.expressen.se/nyheter/brodern-jag-hoppas-han-ruttnar-i-fangelset/")
ci.scrape_article("http://www.nytimes.com/2013/05/14/us/politics/irs-ignored-complaints-on-political-spending-by-big-tax-exempt-groups-watchdog-groups-say.html?hp")
#ci.request_scrape("www.penguin-news.com")
#ci.request_scrape("www.unt.se")
#ci.request_scrape("www.svd.se")
#ci.request_scrape("www.nytimes.com")
#ci.add_newspaper("www.guardian.co.uk")
#ci.add_newspaper("www.nytimes.com")
#ci.add_newspaper("www.unt.se")
#ci.create_newspaper_bank()

#gtdp.parse()


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
