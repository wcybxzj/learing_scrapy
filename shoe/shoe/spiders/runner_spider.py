# -*- coding: utf-8 -*-
__author__ = 'yangbingxi'

from scrapy.contrib.spiders import CrawlSpider
from selenium import webdriver
from shoe.items import RunnerItem

class RunnerSpider(CrawlSpider):
    name = 'shoe'
    allowed_domains = ['roadrunnersports.com']
    start_urls = ['http://www.roadrunnersports.com/rrs/products/BRK1118/']

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        items = []
        self.driver.get(response.url)

        # get colors
        color_tags = self.driver.find_elements_by_class_name('ref2QIColor')
        for color in color_tags:
            item = RunnerItem()
            color.click()
            color_str = self.driver.find_element_by_id('ref2QIColorTitle').text
            item['color'] = color_str

            #get sizes
            size_width_list = []
            size_tags = self.driver.find_elements_by_class_name('ref2QISize')
            for size in size_tags:
                size.click()
                size_str = size.get_attribute('name')

                #get widths
                width_tags = self.driver.find_elements_by_class_name('ref2QIWidth')
                for width in width_tags:
                    width.click()
                    width_str = width.get_attribute('name')
                    availability_tag = self.driver.find_element_by_id('ref2QIInventoryTitleS')
                    size_width_list.append([size_str, width_str, availability_tag.text])

            item['size_width_list'] = size_width_list
            items.append(item)

        self.driver.close()
        yield items