# -*- coding: utf-8 -*-

# Scrapy settings for itzhaopin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'itzhaopin'

SPIDER_MODULES = ['itzhaopin.spiders']
NEWSPIDER_MODULE = 'itzhaopin.spiders'
ITEM_PIPELINES = ['itzhaopin.pipelines.JsonWithEncodingTencentPipeline']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'itzhaopin (+http://www.yourdomain.com)'
