# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from scrapy.http import Request
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import NotConfigured, IgnoreRequest, DropItem
from jikexueyuan.items import JikexueyuanItem
from urlparse import urlparse, urljoin

import os
import time
import random
import MySQLdb
from idfa import DB
import MySQLdb.cursors
from exceptions import IOError
import urllib2
import json

class DataBasePipeline(object):
    "This pipeline used for save iteminfo to mysql"
    def __init__(self):
        self.db1 = DB("127.0.0.1", 3306, "root", "root", "my_jie_data")

    def process_item(self, item, spider):
        sql = "insert into my_jie_spider (id, name , cate_name , subject_name , video_link , video_save_path) values\
            (NULL, %s, %s, %s, %s, %s)"

        params = (item.get('name'), item.get('cate_name'), item.get('subject_name'),
                  item.get('video_link'), item.get('video_save_path'))

        self.db1.insert(sql, params) 
        return item
