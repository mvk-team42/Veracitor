# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'crawler'

SPIDER_MODULES = ['veracitor.crawler.crawler.spiders']
NEWSPIDER_MODULE = 'veracitor.crawler.crawler.spiders'

ITEM_PIPELINES = ['veracitor.crawler.crawler.pipelines.CrawlerPipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'
