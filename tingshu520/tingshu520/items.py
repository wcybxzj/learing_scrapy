# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item

class Tingshu520Item(Item):

    name = Field()
    downlink = Field()
    sound_save_path = Field()
    sound_id = Field()
    user_id = Field()

    # pid = Field()
    # pic_type = Field()
    # title = Field()
    # desc = Field()
    # addtime = Field()
    #
    # user_name = Field()
    # user_id = Field()
    # user_link = Field()
    # profile_img_link = Field()
    # profile_type = Field()
    # origin_img_link = Field()
    #
    # origin_img_save_path = Field()
    # profile_img_save_path = Field()