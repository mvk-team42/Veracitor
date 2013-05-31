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


###TODO###

* Identify dependencies
* Outline the internal structure of the package
* Outline the crawlInterface module
* Describe the testing procedure
