# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from jikexueyuan.items import JikexueyuanItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from selenium import selenium
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import urllib2
import simplejson as json
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


class JkxySpider(Spider):
    name = "jkxy"
    headers = {'Cookie':"SCHOOL_SS__CURRENT=aToyOw%3D%3D; PHPSESSID=n60d9ggc2hcooq9lgm89jgp236; sso_care_tip=1; sso_temp_uid=20141221010956M6-60-10-71-35; sso_eoe_auth=8225s6wmYp5A2%2B6i%2FucnyukNQWmnbelriGgVTSNppCEi11GFm108dOI8lqPL5ocEV8lDSq1w%2Bxl3GqijCWKoW%2FfxI2vGp2J1oewEMA%2BqkRAbsC6k%2FROG8QdRQQoWScB0QmxcjPNhgJIPbma5hpDmBzKY%2BL6suIitUmB%2FycWj; sso_VISIT_CHANNEL=dhjkdgy; sso_ANALYTICS_REVISIT=1; Hm_lvt_f3c68d41bda15331608595c98e9c3915=1429069485,1429069592; Hm_lpvt_f3c68d41bda15331608595c98e9c3915=1429069594; MECHAT_LVTime=1429069593787; MECHAT_CKID=cookieVal=006600142906944597713494; sso_uid=2844579; sso_code=67CIH1; sso_uname=wcybxzj; sso_uhash=1bf2caed8f05718115071d4da439964f"}
    allowed_domains = ["jikexueyuan.com"]
    start_urls = (
        "http://www.jikexueyuan.com/course"
    )

    rules = [
        Rule(sle(allow=("/course/ios/\?pageNum=\d{,4}")), follow=True, callback='parse_item')
    ]

    p_cate = r"/html/body/div[@id='container']/div[@class='wrap w-1000 mar-t20']/div[@id='aside']" \
             r"/div[@class='aside-allCategory']/div[@class='bd']/ul[@class='aside-cList']/li/dl/dd/span/a/@href"

    p_content = "/html/body/div[@id='container']/div[@class='wrap w-1000 ']/div[@id='main']/div[@class='tagGather']" \
                "/div[@class='bd']/div[@class='listbox']/div[@id='changeid']/ul[@class='cf noshow']/li/div/a/@href"

    def start_requests(self):
        yield Request(url=self.start_urls, headers=self.headers, callback=self.parse_type)

    def parse_type(self, response):
        sel = Selector(response)
        links = sel.xpath(self.p_cate).extract()
        for a_href in links:
            a_href = a_href.encode('utf-8')
            link_info = a_href.split("/")
            cate = link_info[-2]
            #print cate
            if a_href =='http://www.jikexueyuan.com/course/ios/':
                yield Request(url=a_href, headers=self.headers, callback=self.parse_item)

            #if re.match(self.patt1, a_item):
            #    g = re.match(self.patt1, a_item).groups()
            #elif re.match(self.patt2, a_item):
            #    g = re.match(self.patt2, a_item).groups()
            #video_link = g[1]
            #down_link = video_link.replace('video', 'down')
            #down_content_link = self.base_url % down_link #打开下载页面的链接
            #yield Request(url=down_content_link, callback=self.get_down_link)

    def parse_item(self, response):
        items = []
        sel = Selector(response)
        content_links = sel.xpath(self.p_content).extract()
        for a_href in content_links:
            item = JikexueyuanItem()
            a_href = a_href.encode('utf-8')
            item['video_link']= a_href
            item['name'] = a_href
            item['video_save_path'] = a_href
            item['sound_id'] = a_href
            item['user_id'] = a_href
            items.append(item)
        return items

