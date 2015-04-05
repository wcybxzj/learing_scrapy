#-*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from tutorial.items import DmozItem

class DmozSpider(BaseSpider):
    '''
        scrapy crawl dmoz -o items.json -t json
    '''
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    #def parse(self, response):
    #    filename = response.url.split("/")[-2]
    #    open(filename, 'wb').write(response.body)

    def parse(self, response):
        hxs = Selector(response)
        sites = hxs.xpath('//fieldset/ul/li')
        #sites = hxs.path('//ul/li')
        items = []

        for site in sites:
           item = DmozItem()
           item['title'] = site.xpath('a/text()').extract()
           item['link'] = site.xpath('a/@href').extract()
           item['desc'] = site.xpath('text()').extract()
           items.append(item)

        return items

