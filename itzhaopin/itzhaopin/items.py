# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItzhaopinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TencentItem(scrapy.Item):
    name = scrapy.Field()                # 职位名称
    catalog = scrapy.Field()             # 职位类别
    workLocation = scrapy.Field()        # 工作地点
    recruitNumber = scrapy.Field()       # 招聘人数
    detailLink = scrapy.Field()          # 职位详情页链接
    publishTime = scrapy.Field()         # 发布时间
