# -*- coding: utf-8 -*-
__author__ = 'yangbingxi'
import re
import json
from scrapy.http import Request
from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle

from jikexueyuan.items import TencentItem, JikexueyuanItem
import re

class JkSpider(CrawlSpider):
    name = "jk"
    allowed_domains = ["jikexueyuan.com"]

    cookies = { 'PHPSESSID':'SCHOOL_SS__CURRENT=aToyOw%3D%3D; PHPSESSID=n60d9ggc2hcooq9lgm89jgp236; sso_care_tip=1; sso_temp_uid=20141221010956M6-60-10-71-35; sso_eoe_auth=8225s6wmYp5A2%2B6i%2FucnyukNQWmnbelriGgVTSNppCEi11GFm108dOI8lqPL5ocEV8lDSq1w%2Bxl3GqijCWKoW%2FfxI2vGp2J1oewEMA%2BqkRAbsC6k%2FROG8QdRQQoWScB0QmxcjPNhgJIPbma5hpDmBzKY%2BL6suIitUmB%2FycWj; sso_VISIT_CHANNEL=dhjkdgy; sso_ANALYTICS_REVISIT=1; Hm_lvt_f3c68d41bda15331608595c98e9c3915=1429069485,1429069592; Hm_lpvt_f3c68d41bda15331608595c98e9c3915=1429069594; MECHAT_LVTime=1429069593787; MECHAT_CKID=cookieVal=006600142906944597713494; sso_uid=2844579; sso_code=67CIH1; sso_uname=wcybxzj; sso_uhash=1bf2caed8f05718115071d4da439964f' }

    start_urls = [
        "http://www.jikexueyuan.com/course/ios/"
    ]

    rules = [
        Rule(sle(allow=("/course/ios/\?pageNum=\d{,4}")), follow=True, callback='parse_item')
    ]

    p_subject_href = "/html/body/div[@id='container']/div[@class='wrap w-1000 ']/div[@id='main']/div[@class='tagGather']" \
                "/div[@class='bd']/div[@class='listbox']/div[@id='changeid']/ul[@class='cf noshow']/li/div/a/@href"

    p_subject_name = "//h2/a/text()"

    def parse_item(self, response):
        sel = Selector(response)
        subject_hrefs = sel.xpath(self.p_subject_href).extract()
        subject_names = sel.xpath(self.p_subject_name).extract()
        sub_hrefs = []
        for sub_href in subject_hrefs:
            sub_href = sub_href.encode('utf-8')
            #print '列表页面:'
            #print sub_href
            yield Request(url=sub_href, cookies=self.cookies,  callback=self.parse_subject_list)

    def parse_subject_list(self, response):
        sel = Selector(response)
        final_href = r"/html/body/div[@class='lesson-table cf']/div[@class='video-list']/div[@class='lesson-box'][1]/ul/li/div[@class='text-box']/h2/a/@href"
        hrefs = sel.xpath(final_href).extract()
        for href in hrefs:
            href = href.encode('utf-8')
            yield Request(url=href, cookies=self.cookies, callback=self.parse_content)

    def parse_content(self, response):
        item = JikexueyuanItem()
        sel = Selector(response)
        bodys = sel.xpath(r"//body").extract()
        #分类名
        patt_cat_name = r"/html/body/div[@id='palyer-box']/h1/text()"
        item['cate_name']= sel.xpath(patt_cat_name).extract()
        #专题名
        patt_subject_name = r"/html/body/div[@class='crumbs']/div[@class='w-1000']/a[4]/text()"
        item['subject_name']= sel.xpath(patt_subject_name).extract()
        #名字
        patt_name = r"/html/body/div[@id='palyer-box']/h1/text()"
        item['name']= sel.xpath(patt_subject_name).extract()

        patt_one = r'(.*)<source src="(\S+)" type="video/mp4" />(.*)'
        patt_two = r'(.*)<source src="(\S+)" type="video/mp4">(.*)'
        for body in bodys:
            body = "".join(body.splitlines())
            m = re.match(patt_one, body)
            if m:
                g = m.groups()
                item['video_link'] = g[1]
            else:
                m = re.match(patt_two, body)
                if m:
                    g = m.groups()
                    item['video_link'] = g[1]
        return item

