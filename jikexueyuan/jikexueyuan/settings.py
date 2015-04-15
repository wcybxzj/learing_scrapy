# Scrapy settings for miaopai project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os

BOT_NAME = 'jikexueyuan'

SPIDER_MODULES = ['jikexueyuan.spiders']
NEWSPIDER_MODULE = 'jikexueyuan.spiders'

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
COOKIES_ENABLED = True

ITEM_PIPELINES = [ 'jikexueyuan.mediafile.JkxySpiderFile',
                    'jikexueyuan.pipelines.DataBasePipeline', ]

IMAGES_STORE = '/data/html/capture/jkxy/images'
IMAGES_EXPIRES = 30
IMAGES_THUMBS = {
	'small': (50, 50),
	'big': (270, 270),
}
IMAGES_MIN_HEIGHT = 0
IMAGES_MIN_WIDTH = 0

FILE_STORE = '/data/html/capture/jkxy/files'
MEDIA_FILE_STORE = '/data/html/capture/jkxy/videos'
FILE_EXPIRES = 90
MEDIA_FILE_EXPIRES = 90
FILE_EXTENTION = ['.flv','hd2','.mp4', '.swf','.mov',]

#For more mime types about file,you can visit:
#http://mimeapplication.net/
MEDIA_FILE_CONTENT_TYPE = ['application/file',
	'video/3gpp',
	'video/avi',
	'video/dvd',
	'video/mp4v-es',
	'video/mp4',
	'video/mpeg',
	'video/mpeg2',
	'video/mpg',
	'video/quicktime',
	'video/x-flv',
	'video/flv',
    'video/sgi-movie',
    'video/x-quicktime',
    'video/vnd.sealedmedia.softseal.mov',
    'video/x-sgi-movie',
    'application/octet-stream',
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

USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31'
DOWNLOADER_MIDDLEWARES = {
	'jikexueyuan.rotate_useragent.RotateUserAgentMiddleware':400,
}

#DUPEFILTER_CLASS = 'miaopai.dupefilter.SeenURLFilter'
CONCURRENT_REQUESTS = 16
CONCURRENT_ITEMS = 100

JOBDIR='/data/mytext/jkxy'
DUPEFILTER_DEBUG = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'miaopai (+http://www.yourdomain.com)'
