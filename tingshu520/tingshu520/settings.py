# Scrapy settings for ximalaya project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os

BOT_NAME = 'tingshu520'

SPIDER_MODULES = ['tingshu520.spiders']
NEWSPIDER_MODULE = 'tingshu520.spiders'

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
COOKIES_ENABLED = True

ITEM_PIPELINES = [
                    #'tingshu520.pipelines.XimalayaPipeline',
                    'tingshu520.mediafile.XmlySpiderFile',
                    'tingshu520.pipelines.DataBasePipeline'
                 ]

IMAGES_STORE = '/data/html/capture/xmly/images'
IMAGES_EXPIRES = 30
IMAGES_THUMBS = {
	'small': (50, 50),
	'big': (270, 270),
}
IMAGES_MIN_HEIGHT = 0
IMAGES_MIN_WIDTH = 0

FILE_STORE = '/data/html/capture/xmly/files'
MEDIA_FILE_STORE = '/data/html/capture/xmly/sounds'
FILE_EXPIRES = 90
MEDIA_FILE_EXPIRES = 90
FILE_EXTENTION = ['.flv','hd2','.mp4', '.swf','.mp3','f4v']

#For more mime types about file,you can visit:
#http://mimeapplication.net/
MEDIA_FILE_CONTENT_TYPE = ['application/file',
    'application/octet-stream',
    'audio/mp3',
    'audio/f4v',
    'audio/mpeg',
    'audio/mpeg3',
    'audio/mog',
    'audio/x-mp3',
    'audio/x-mpeg',
    'audio/x-mpeg3',
    'audio/x-mpegaudio',
    'audio/x-mpg',
    ]

URL_GBK_DOMAIN = []
ATTACHMENT_FILENAME_UTF8_DOMAIN = []

DOWNLOAD_TIMEOUT = 600

#for httpcache
#HTTPCACHE_ENABLED = True
#HTTPCACHE_POLICY = 'scrapy.contrib.httpcache.RFC2616Policy'
#HTTPCACHE_STORAGE = 'scrapy.contrib.httpcache.FilesystemCacheStorage'
#HTTPCACHE_IGNORE_MISSING = False
#HTTPCACHE_DIR = '/data1/scrapy/httpcache/cache' 

#WEBKIT_DOWNLOADER=['kapookspider']
USER_AGENT = 'wget'
#USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31'

#DUPEFILTER_CLASS = 'ximalaya.dupefilter.SeenURLFilter'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ximalaya (+http://www.yourdomain.com)'
