import os
from os.path import realpath, dirname

import veracitor.crawler.crawlInterface as ci
import veracitor.crawler.gtdParser as gtdp
from veracitor.database import *
from veracitor.logger import logger

#run tests

current_dir = dirname(realpath(__file__))

# Setup some database data
os.system("python " + current_dir + "/setup_data.py")

networkModel.build_network_from_db()


#tags = ["General","Crime","Culture","Politics","Sports","Finances"]
#for tag in tags:
    #extractor.get_tag_create_if_needed(tag)

#print "string is " + str(information.Information.objects(url='http://www.dn.se/sport/ishockey/detroit-tillbaka-pa-slutspelsplats-1'))

#logger.log("testing",logger.Level.debug,logger.Area.crawler)

#ci.set_callback(a)
ci.init_interface()
#ci.add_newspaper("www.svd.se")
#ci.add_newspaper("www.dn.se")
#ci.add_newspaper("www.guardian.co.uk")
#ci.add_newspaper("www.gp.se")
#ci.add_newspaper("www.staffordshirenewsletter.co.uk")
#ci.add_newspaper("www.nytimes.com")
#ci.add_newspaper("www.washingtonpost.com")
#ci.add_newspaper("www.chicagotribune.com")
#ci.add_newspaper("www.dailynews.com")
#ci.add_newspaper("www.latimes.com")
#ci.add_newspaper("www.guardian.co.uk")
#ci.add_newspaper("www.nytimes.com")
#ci.add_newspaper("www.unt.se")
#ci.add_newspaper("www.penguin-news.com")


#ci.scrape_article("http://www.dn.se/nyheter/varlden/nordkoreaexpert-varre-an-pa-mycket-lange")
#ci.scrape_article("http://www.svd.se/nyheter/inrikes/mamman-dog-i-vantan-pa-dottern_8152288.svd")
#ci.scrape_article("http://www.guardian.co.uk/uk/2013/may/07/jimmy-tarbuck-arrested-allegation-assault-teenage-boy")
#ci.scrape_article("http://www.svd.se/nyheter/inrikes/utbrett-fiskfusk-avslojat_8046058.svd")
#ci.scrape_article("http://www.dn.se/nyheter/sverige/barn-som-sett-vald-utan-ersattning")
#ci.scrape_article("http://www.nytimes.com/2013/05/10/us/disease-threatens-floridas-citrus-industry.html?hp&_r=0")
#ci.scrape_article("http://www.washingtonpost.com/politics/irs-targeted-groups-critical-of-government-documents-from-agency-probe-show/2013/05/12/bb38e5bc-bb24-11e2-97d4-a479289a31f9_story.html")
#ci.scrape_article("http://www.washingtonpost.com/world/middle_east/sectarianism-in-iraq-stoked-by-syrian-war/2013/05/16/b74161da-bc98-11e2-9b09-1638acc3942e_story.html?hpid=z1")
#ci.scrape_article("http://www.washingtonpost.com/politics/fbi-seeks-source-of-prostitution-corruption-allegations-against-sen-robert-menendez/2013/05/16/72ad79a0-bbda-11e2-89c9-3be8095fe767_story.html?hpid=z1") # ok!
#ci.scrape_article("http://www.washingtonpost.com/blogs/fact-checker/post/holders-incorrect-claim-on-the-fast-and-furious-criminal-citation-decision/2013/05/16/d15f26cc-be7a-11e2-97d4-a479289a31f9_blog.html?hpid=z4")
#ci.scrape_article("http://www.expressen.se/nyheter/brodern-jag-hoppas-han-ruttnar-i-fangelset/")
#ci.scrape_article("http://www.nytimes.com/2013/05/14/us/politics/irs-ignored-complaints-on-political-spending-by-big-tax-exempt-groups-watchdog-groups-say.html?hp")


#ci.request_scrape("www.penguin-news.com")
#ci.request_scrape("www.unt.se")
#ci.request_scrape("www.svd.se")
#ci.request_scrape("www.nytimes.com")
#ci.request_scrape("www.washingtonpost.com")
#ci.request_scrape("www.chicagotribune.com")
#ci.request_scrape("www.latimes.com")


#ci._test_rss("http://penguin-news.com/index.php?format=feed&type=rss")
ci._test_rss("http://www.dn.se/nyheter/m/rss/senaste-nytt")
#ci.start_continuous_scrape()

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
