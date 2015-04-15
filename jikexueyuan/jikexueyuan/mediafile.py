#!/usr/bin/python
#-*-coding:utf-8-*-

import os
import itertools
from scrapy import log
from scrapy.item import Item
from pprint import pprint
from scrapy.http import Request
from scrapy.utils.misc import arg_to_iter
from twisted.internet.defer import Deferred, DeferredList
from select_result import list_first_item
from file import FilePipeline,FSFilesStore,FileException
from scrapy.exceptions import DropItem, NotConfigured
from jikexueyuan.items import JikexueyuanItem

class NofilesDrop(DropItem):
    """Product with no files exception"""
    def __init__(self, original_url="", *args):
        self.original_url = original_url
        DropItem.__init__(self, *args)

    def __str__(self):#####for usage: print e
        print "DROP(NofilesDrop):" + self.original_url

        return DropItem.__str__(self)

class BookFileException(FileException):
    """General book file error exception"""

class FSBookFilesStore(FSFilesStore):
    pass

class JkxySpiderFile(FilePipeline):
    """
        This is for download the book file and then define the book_file 
        field to the file's path in the file system.
    """

    MEDIA_NAME = 'mediafile'
    EXPIRES = 180
    MEDIA_FILE_CONTENT_TYPE = []
    URL_GBK_DOMAIN = []
    ATTACHMENT_FILENAME_UTF8_DOMAIN = []
    STORE_SCHEMES = {
        '': FSBookFilesStore,
        'file': FSBookFilesStore,
    }
    
    FILE_EXTENTION = ['.flv','.hd2','.mp4','.swf','.mov',]

    def __init__(self,store_uri,download_func=None):
        super(JkxySpiderFile, self).__init__(store_uri=store_uri,download_func=download_func)
        if not store_uri:
            raise NotConfigured
        self.bookfile_store = store_uri
        self.store = self._get_store(store_uri)
        self.item_download = {}
        self.count = 0

    @classmethod
    def from_settings(cls, settings):
        cls.EXPIRES = settings.getint('MEDIA_FILE_EXPIRES', 180)
        cls.MEDIA_FILE_CONTENT_TYPE = settings.get('MEDIA_FILE_CONTENT_TYPE',[])
        cls.ATTACHMENT_FILENAME_UTF8_DOMAIN = settings.get('ATTACHMENT_FILENAME_UTF8_DOMAIN',[])
        cls.URL_GBK_DOMAIN = settings.get('URL_GBK_DOMAIN',[])
        cls.FILE_EXTENTION = settings.get('FILE_EXTENTION',[])
        store_uri = settings['MEDIA_FILE_STORE']
        return cls(store_uri)

    def process_item(self, item, spider):
        """
            custom process_item func,so it will manage the Request result.
        """
        if item.get('video_link') is None:
            raise NofilesDrop
        info = self.spiderinfo
        requests = arg_to_iter(self.get_media_requests(item, info))
        dlist = [self._process_request(r, info) for r in requests]
        dfd = DeferredList(dlist, consumeErrors=1)
        dfd.addCallback(self.item_completed, item, info)
        return dfd.addCallback(self.another_process_item, item, info)

    def another_process_item(self, result, item, info):
        """
            custom process_item func,so it will manage the Request result.
        """
        
        assert isinstance(result, (Item, Request)), \
                    "pipeline' item_completed must return Item or Request, got %s" % \
                    (type(result))
        if isinstance(result,Item):
            return result
        elif isinstance(result,Request):
            dlist = [self._process_request(r, info) for r in arg_to_iter(result)]
            dfd = DeferredList(dlist, consumeErrors=1)
            dfd.addCallback(self.item_completed, item, info)
            #XXX:This will cause one item maybe return many times,it depends on how many 
            #times the download url failed.But it doesn't matter.Because when raise errors,
            #the items are no longer processed by further pipeline components.And when all
            #url download failed we can drop that item which book_file or book_file_url are
            #empty.
            return dfd.addCallback(self.another_process_item, item, info)
        else:
            raise NofilesDrop

    def get_media_requests(self, item, info):
        """
            Only download once per book,so it pick out one from all of the download urls.
        """ 
        
        #XXX:To test specific url,you can use the following method:
        if item.get('video_link'):
            yield Request(item.get('video_link'), dont_filter=True)

    def item_completed(self, results, item, info):
        if self.LOG_FAILED_RESULTS:
            msg = '%s found errors proessing %s' % (self.__class__.__name__, item)
            for ok, value in results:
                if not ok:
                    log.err(value, msg, spider=info.spider)

        base = "http://182.92.111.153/capture/miaopai/videos"
        file_paths_urls = [(x['path'],x['url']) for ok, x in results if ok]
        file_path_url = list_first_item(file_paths_urls)
        if file_path_url:
            sub = file_path_url[1].split('/')[-1]
            conpath = file_path_url[0] + '/' +sub
            item['video_save_path'] = os.path.join(base, conpath)
        return item
        
    def is_valid_content_type(self,response):
        """
            judge whether is it a valid response by the Content-Type.
        """
        content_type = response.headers.get('Content-Type','')
        
        return content_type not in self.MEDIA_FILE_CONTENT_TYPE
