#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'yangbingxi'
import urllib2, httplib
import openanything

httplib.HTTPConnection.debuglevel = 1
request = urllib2.Request('http://www.baidu.com')
opener = urllib2.build_opener(openanything.DefaultErrorHandler())
firstdatastream = opener.open(request)
print firstdatastream.headers.dict
