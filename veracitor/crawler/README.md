The Crawler Package
===================
The crawler package aims to provide web crawling functionality to the project in order to gather information about various web resources.
It does this by utilizing the [Scrapy](http://scrapy.org) framework.

The crawlInterface module
-------------------------
The main way of using the crawler package is by utilizing the crawlInterface module.

The module exposes the following methods:

#####add_newspaper(url)
Scrapes the given url and tries to gather metadata about the site, such as a title, description and any rss-feeds it might have.
The data is then added to the database as a producer object.
It is expected (and not checked) that the url points to an actual news site.

#####scrape_article(url)
Scrapes the given url as an article (information object) and tries to extract relevant data such as title, a summary, date published, author etc.
Only if the webpage is deemed to contain a news article, will it be scraped.
This decision is made using the article-qualification xpaths defined in webpageMeta.xml.
If data is scraped, it is then added to the database as an information object.
As a side-effect the domain is added to the database as a producer if it did not exist already in the same way as if `add_newspaper(url)` had been invoked on the domains base-url.


#####request_scrape(url)
Crawls the given url, following any links found on the page within the same domain and trying to scrape the pages as articles in the same way as `scrape_article(url)`.
It only follows links to depth 1 since the increase in data is practically exponential.
Also adds the url as a producer in the same way as `add_newspaper(url)` would if it did not already exist.

#####create_newspaper_bank(url)
Crawls [listofnewspapers.com](http://www.listofnewspapers.com) for newspapers located in the United Kingdom, North America and Sweden, since only english and swedish is supported in the parsing stage.
The newspapers are added to the database in the same way as `add_newspaper(url)` would have.

#####scrape_all_in_bank(url)
Iterates through the webpages listed in the WebpageMeta.xml file.
If the webpage has an rss-feed the feed is scraped and information objects are added.
If no rss-feed has been found for that producer, a `request_scrape(url)` is performed for that url.

Internal structure
------------------

Dependencies
------------

####Internal####
* Scrapy==0.16.4
* Twisted==12.3.0
* Openpyxl==1.6.2 (for gtdParser module)
* ...

####External####
To properly be able to test the package via the crawlInterface module the Veracitor database package is needed and all its dependencies has to be fullfilled.

To parse the GTD database, download the excel-file and put it in the crawler package directory. Make sure there are no negative values for date (this was encountered and produces an error).

Testing
-------
Testing can be done via the crawler_test.py file in the root directory of Veracitor.
This bypasses the celery framework for easier debugging regarding scraped data.
From the crawler_test.py file, import the crawlInterface module and the gtdParser module as needed.
The database package has to be imported as well.
```Python
import veracitor.crawler.crawlInterface as ci
import veracitor.crawler.gtdParser as gtdp
from veracitor.database import *
```

Initialize global network? (behövs det verkligen fortfarande?)

To enable easier debugging, call the `init_interface()` method, this binds a callback for scraped items to the scrapy log facility.
```Python
ci.init_interface()
```

The crawlInterface can now be directly accessed by calling its methods.
Example:
```Python
ci.add_newspaper("www.washingtonpost.com")
ci.scrape_article("www.washingtonpost.com/some/article")
ci.request_scrape("www.washingtonpost.com")
...
```
When the tests are set up, simply run the crawler_test.py file as a python script:
`python crawler_test.py`

###TODO###

* Identify dependencies
* Outline the internal structure of the package
