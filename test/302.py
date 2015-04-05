#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import urllib2
import httplib
import openanything

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


httplib.HTTPConnection.debuglevel = 1

url = 'http://www.520tingshu.com/down1/tudou.asp?id=207080894'
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
print f.code #添加header 302, 不添加header 503
print f.headers.dict['location']
print type(f.headers.dict['location'])
#print f.read()