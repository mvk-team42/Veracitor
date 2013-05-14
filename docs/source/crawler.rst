:mod:`crawler` -- Crawler
=========================

The Crawler module uses the Scrapy(http://scrapy.org) framework internally.
The crawlInterface module acts as the main interface for the webcrawling functionality.
It dispatches a spider to the given url when a method is called.

The gtdParser module is solely used for parsing the GTD database from an excel file.
This has to be run manually and is not a part of Veracitor as a whole.

The webpageMeta module provides an interface to an xml-file in which vital information regarding webpages and how they should be crawled are stored.

:mod:`crawlInterface` -- Interface for the crawler
--------------------------------------------------

.. automodule:: veracitor.crawler.crawlInterface
   :members:

:mod:`gtdParser` -- Parsing of GTD
----------------------------------

.. automodule:: veracitor.crawler.gtdParser
   :members:

:mod:`webpageMeta` -- Interface for webpage metadata and xpaths
---------------------------------------------------------------

.. automodule:: veracitor.crawler.crawler.webpageMeta
   :members:

Spiders
+++++++

Spiders mostly use the scrape methods defined in the utils module to parse the responses they recieve.

:mod:`utils` -- Common utility-methods for spiders
--------------------------------------------------
.. automodule:: veracitor.crawler.crawler.spiders.utils
   :members:

:mod:`articleSpider` -- Article spider
--------------------------------------
.. automodule:: veracitor.crawler.crawler.spiders.articleSpider
   :members:

:mod:`metaNewspaperSpider` -- Newspaper metainformation spider
--------------------------------------------------------------
.. automodule:: veracitor.crawler.crawler.spiders.metaNewspaperSpider
   :members:

:mod:`newspaperSpider` -- Newspaper spider
------------------------------------------
.. automodule:: veracitor.crawler.crawler.spiders.newspaperSpider
   :members:

:mod:`newspaperBankSpider` -- Newspaper bank spider
---------------------------------------------------
.. automodule:: veracitor.crawler.crawler.spiders.newspaperBankSpider
   :members:

:mod:`rssSpider` -- RSS spider
------------------------------
.. automodule:: veracitor.crawler.crawler.spiders.rssSpider
   :members:

Items
+++++

There are two items used by the Crawler module. ArticleItem is for scraping infomation objects and ProducerItem for scraping producers.
The items are sent to their respective pipelines when scraped, which process them accordingly.

:mod:`items` -- Items
---------------------
.. automodule:: veracitor.crawler.crawler.items
   :members:

:mod:`pipelines` -- Wrapper for pipelines
-----------------------------------------
.. automodule:: veracitor.crawler.crawler.pipelines
   :members:

:mod:`producerPipeline` -- Pipeline for ProducerItem
----------------------------------------------------
.. automodule:: veracitor.crawler.crawler.producerPipeline
   :members:

:mod:`articlePipeline` -- Pipeline for ArticleItem
--------------------------------------------------
.. automodule:: veracitor.crawler.crawler.articlePipeline
   :members:
