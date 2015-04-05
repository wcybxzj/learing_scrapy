# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from scrapy.http import Request
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import NotConfigured, IgnoreRequest, DropItem

import os
import time
import MySQLdb
from idfa import DB
import MySQLdb.cursors
from exceptions import IOError

class XimalayaPipeline(ImagesPipeline):
    "This pipeline used for save download images for KapookSpider"
    def __init__(self, store_uri, download_func=None):
        self.image_store = store_uri
        super(XimalayaPipeline, self).__init__(store_uri, download_func=None)
        self.base = "http://182.92.111.153/capture/xmly/images/"

    def get_media_requests(self, item, info):
        if item.get('profile_img_url') and item.get('sound_img_link'):
            yield Request(item.get('sound_img_link'))
            yield Request(item.get('profile_img_url')) 
        else:
            raise DropItem('Item images not complete')
	
    def item_completed(self, results, item, info):
        image_paths = [x ['path'] for ok, x in results if ok]
        if not image_paths:
            print "Item contains no images"
        if len(image_paths) == 2:
            item['sound_img_save_path'] , item['profile_img_save_path']= [self.base + i for i in image_paths]
            return item
        else:
            raise DropItem('Image download not complete')

class DataBasePipeline(object):
    "This pipeline used for save iteminfo to mysql"
    def __init__(self):
        self.db1 = DB("127.0.0.1", 3306, "root", "root", "my_jie_data")
        self.is_subscribe = 0

    def process_item(self, item, spider):
        if item.get('name'):
            #user_id = self.select_from_admin(item)
            item['user_id'] = 123
            ret = self.insertTable(item, item['user_id'])
            return item

    def insert_user_table(self, item):
        #name header
        sql_sel = "select uid from user where name = %s and header = %s"
        if len(item.get("user_name")) != 0:
            params = (item.get("user_name"), item.get("profile_img_url"))
        else:
            params = (item.get("user_name"), item.get("profile_img_url"))
        res1 = self.db1.query(sql_sel, params)
        if res1 == ():
            sql_ins = "insert into user (name, header) values (%s, %s)"
            res0 = self.db1.insert(sql_ins, params)
            return self.db1.query(sql_sel, params)[0]['uid']
        else:
           return res1[0]['uid']

    def select_from_admin(self, item):
        #youku
        key = "open_id"
        sql = "select %s from open_platform where open_id = %s and screen_name = %s \
                and type = 4 and source = 31" 
        params = (key, item.get('user_id'), item.get('user_name'))
        res = self.db1.query(sql, params)
        if res == ():
        #create jie user table;
        #user add, get uid, and add open_platform a item 
            zombie_uid =  self.insert_user_table(item)

            ins_sql = "insert into open_platform (open_id, screen_name, type, source, zombie_uid) values (%s, %s, %s, %s, %s)"
            params = (item.get('user_id'), item.get('user_name'), 4, 31, zombie_uid)
            self.db1.insert(ins_sql, params)

            self.check_open_id(zombie_uid, item.get('user_name'))
            return zombie_uid
        else:
            zombie_uid = self.insert_user_table(item)
            self.check_open_id(zombie_uid, item.get('user_name'))
            
            return zombie_uid

    def check_open_id(self, zombie_uid, user_name):
        sel_sql = "select * from subscribe_manage where uid = %s"%zombie_uid
        if self.db1.query(sel_sql, None) == ():
            sel_ins = "insert into subscribe_manage (uid, category_id, nickname) value (%s, %s, %s)"
            params = (zombie_uid, 13, user_name)
            self.db1.insert(sel_ins, params)
            self.is_subscribe = 1
        else:
            self.is_subscribe = 1

    def insertTable(self, item, user_id):
        current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        id_sql = "insert into g_value(`tmpnum`) Value('10000')"
        id = self.db1.insert(id_sql, None)
        with open('g_value.txt','a+') as f:
            f.write(str(id)+' '+current+'\n')

        sel_sql = "select id from jie_spider where mid = %s and user_id = %s and `from`=31"
        params = (item.get('sound_id'), user_id)
        res = self.db1.query(sel_sql, params)
        if res != ():
            return item

        sql = "insert into jie_spider (id, created_at, mid, text, image0, video_url, screen_name, name, profile_image,\
        uid, url, weight, `from`,addtime,original_image, type, user_id, user_type, status) values ( %s, %s, %s, %s, %s, %s, %s, %s,\
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (id, current, item.get('sound_id'), item.get('name')[0], item.get('sound_img_save_path', ''),
        item.get('sound_save_path'), item.get('user_name', ''), item.get('user_name', ''),\
        item.get('profile_img_save_path', ''), item.get('user_id'),item.get('user_link', ''), 4, 31, item.get('publish_date', ''),\
        item.get('sound_img_save_path', ''), 31, user_id, self.is_subscribe, 4)

        print "========================================"
        print sql %params

        return self.db1.insert(sql, params) 
