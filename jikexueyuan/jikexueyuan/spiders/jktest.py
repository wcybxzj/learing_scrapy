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

class JktestSpider(CrawlSpider):
    name = "jktest"
    allowed_domains = ["jikexueyuan.com"]

    cookies = { 'PHPSESSID':'21265nihgh69r3visvcqv4s4h1','sso_care_tip':'1','sso_temp_uid':'20141221010956M6-60-10-71-35','sso_eoe_auth':'ad27Ex4SjNt2kZtgdlPQMQgWmPpIGtYb6ybdS5bj22hk1JUt3l%2FlauAkwbncmRxH%2B%2BD1ebOOMG42PQQQxAJRTOQ8P2RZ2sv6r9ZUf8gnzNbfYtV6i4L0FncmQDWxuJuMhWpKB%2BoV7apOYwdgqr3%2FgX1YnsFv7DcI%2Bj23Wgrz','sso_uid':'2844579','sso_code':'67CIH1','sso_uname':'wcybxzj','sso_uhash':'1bf2caed8f05718115071d4da439964f','sso_VISIT_CHANNEL':'cocoszs','sso_ANALYTICS_REVISIT':'1','Hm_lvt_f3c68d41bda15331608595c98e9c3915':'1428826334,1428826447,1428899482,1428902617','Hm_lpvt_f3c68d41bda15331608595c98e9c3915':'1428902624','MECHAT_LVTime':'1428902624174','MECHAT_CKID':'cookieVal' }



    start_urls = "http://www.jikexueyuan.com/course/ios/"
    
    
    def start_requests(self):
        yield Request(url=self.start_urls, cookies=self.cookies, callback=self.parse_item) 

    def parse_item(self, response):
        sel = Selector(response)
        print sel.xpath(r'//body').extract()

