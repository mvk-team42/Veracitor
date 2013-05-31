The Crawler Package
===================
The crawler package aims to provide web crawling functionality to the project in order to gather information about various web resources.
It does this by utilizing the [Scrapy](http://scrapy.org) framework.

The crawlInterface module
-------------------------
The main way of using the crawler package is by utilizing the crawlInterface module.

Methods: ....

#####add_newspaper(url)
etc....

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
To properly be able to test the package via the crawlInterface module the Veracitor database package is needed.

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
* Outline the crawlInterface module
* Describe the testing procedure
