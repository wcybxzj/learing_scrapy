# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from tingshu520.items import Tingshu520Item
from scrapy.contrib.spiders import CrawlSpider, Rule
from selenium import selenium
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import urllib2
try:
    import simplejson as json
except (ImportError,):
    import json
from urlparse import urljoin, urlparse
import re

class TingshuSpider(Spider):
    name = "tingshu"
    allowed_domains = ["520tingshu.com"]
    start_urls = (
        'http://www.520tingshu.com/video/?11502-0-0.html'
    )

    patt1 = r'<a title="(\S+)" href="(\S+)" style="color:red" target="_blank">(\S+)</a>'
    patt2 = r'<a title="(\S+)" href="(\S+)" target="_blank">(\S+)</a>'
    base_url = 'http://www.520tingshu.com%s'

    def start_requests(self):
        yield Request(url=self.start_urls, callback=self.next_parse)

    def next_parse(self, response):
        sel = Selector(response)
        content_links = sel.xpath("//div[@class='playurl']//a").extract()
        for a_item in content_links:
            a_item = a_item.encode('utf-8')
            if re.match(self.patt1, a_item):
                g = re.match(self.patt1, a_item).groups()
            elif re.match(self.patt2, a_item):
                g = re.match(self.patt2, a_item).groups()
            video_link = g[1]
            down_link = video_link.replace('video', 'down')
            down_content_link = self.base_url % down_link #打开下载页面的链接
            yield Request(url=down_content_link, callback=self.get_down_link)

    def get_down_link(self, response):
        sel = Selector(response)
        all_script_links = sel.xpath("//script/@src").re(u'/playdata/\d+/\d+.js')
        name = sel.xpath("//div[@class='moviecont']/div[1]/text()").extract()
        down_content_link = response.url

        for url in all_script_links:
            request_url = self.base_url % url
            OriginalThisUrlData = urllib2.urlopen(request_url).read().decode('gbk')

            patt = r'(var VideoListJson=)(.+),urlinfo'
            result = re.match(patt, OriginalThisUrlData).groups()
            VideoListJson = result[1]
            VideoListJson = VideoListJson.replace("'", '"')
            VideoListJson = json.loads(VideoListJson)

            ThisUrl=''
            sid = down_content_link.split("-")
            n = len(sid)

            for i in range(n):
                ThisUrl += sid[i]+'-'
            vid = int(sid[n-1].split(".")[0])
            pid = int(sid[n-2])

            sStr =  VideoListJson[pid][1][vid]
            uArr = sStr.split("$")
            if uArr[2]=='tudou':
               Url='http://www.520tingshu.com/down1/tudou.asp?id='+uArr[1]
            else:
               Url = uArr[1]

            item = Tingshu520Item()
            item['name'] = name
            item['downlink'] = self.get_downf4v_link(Url)
            item['sound_id'] = self.get_sound_id(name[0])
            yield item

    '''
    function getHtmlParas(str){
        var ss = window.location.href;
        var sid = ss.split('-');
        var n = sid.length;
        for(var i=0;i<n-1;i++){
            ThisUrl+=sid[i]+'-';
        }
        var vid = sid[n-1].split(".")[0];
        var pid = sid[n-2];
        var sArr = new Array(vid,pid);
        return sArr;
    }
    '''
    def js_getHtmlParas(self, href, ThisUrlData):
        pass


    '''
    unction viewplay(vid,pid){
        var sStr = VideoListJson[pid][1][vid];
        var S;
        Pn =  VideoListJson[pid][1].length;

        var uArr = sStr.split("$");
        if(uArr[2]=='tudou'){
           Url='http://www.520tingshu.com/down1/tudou.asp?id='+uArr[1] ;
        }else{
           Url = uArr[1] ;
        }

        var fUrl = Url;
        var thunder_url = Url;
        S = '<script src="http://ufile.qushimeiti.com/Flashget_union.php?fg_uid=96788"></script><script src="/js/tingfree/Flashget_base64.js"></script><div class="new_downlist"><ul>';
        S += '<li class="local"><a href="'+Url+'" target="_blank">本地下载</a></li>';
    }
    '''
    def js_viewplay(vid, pid):
        pass

    def get_downf4v_link(self, url):
        #url = 'http://www.520tingshu.com/down1/tudou.asp?id=207080894'
        req = urllib2.Request(url)

        req.add_header('Host', 'www.520tingshu.com')
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:31.0) Gecko/20100101 Firefox/31.0')
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        req.add_header('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3')
        req.add_header('Accept-Encoding', 'gzip, deflate')
        req.add_header('Referer', 'http://www.520tingshu.com/down/?11502-0-0.html')
        req.add_header('Cookie', 'MAX_HISTORY={video:[{"name":"\u4E8E\u516C\u6848","link":"http://www.520tingshu.com/book/book11502.html","pic":"/pic/uploadimg/2014-9/20149197104725122.jpg"},{"name":"\u9EC4\u6CB3\u53E4\u4E8B","link":"http://www.520tingshu.com/book/book11751.html","pic":"/pic/uploadimg/2014-10/20141031812543930.jpg"}]}; bdshare_firstime=1426436559317; Hm_lvt_8d4e1ce243d40f33c6ca050451a189f2=1426436562,1426786484; CNZZDATA3830836=cnzz_eid%3D1926779155-1426432488-%26ntime%3D1426783939; ASPSESSIONIDSSQTDCQD=EANNDKHBBFGBIGOPGGGJEEHP; Hm_lpvt_8d4e1ce243d40f33c6ca050451a189f2=1426786484; hm_t_vis_54806=0')
        req.add_header('Connection', 'keep-alive')

        opener = urllib2.build_opener(MyHTTPErrorProcessor)
        f = opener.open(req)
        #print f.code #添加header 302, 不添加header 503
        return f.headers.dict['location']
        #print f.read()

    def get_sound_id(self, original_name):
        patt_id = r'(.+?)(\d{1,5})(.+?)'
        data_for_id = re.match(patt_id, original_name).groups()
        return data_for_id[1]

class MyHTTPErrorProcessor(urllib2.HTTPErrorProcessor):

    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()

        # only add this line to stop 302 redirection.
        if code == 302: return response

        if not (200 <= code < 300):
            response = self.parent.error(
                'http', request, response, code, msg, hdrs)
        return response

    https_response = http_response
