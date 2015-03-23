#encoding=utf-8
import os
import urllib
import urllib2
import poster
import cookielib
import zlib
from bs4 import BeautifulSoup
import re
from PIL import Image
import StringIO
import mimetypes
import mimetools


def up_pic_header_built(req, body=None, content_type=None):
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Connection', 'Keep-Alive')
    # req.add_header('Origin', 'http://127.0.0.1:8069')
    req.add_header('Referer', 'http://127.0.0.1:8069/web/login')
    req.add_header('User-Agent', 'fake-client')
    if content_type:
        req.add_header('Content-Type', content_type)
    if body:
        req.add_header('Content-Length', str(len(body)))

def gzip_built(response):
    res_html = response.read()
    # print res_html
    if response.info().get('Content-Encoding') == 'gzip':
        res_html = zlib.decompress(res_html, 16+zlib.MAX_WBITS)
        # print res_html
    return res_html

#debug日志
httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
cj = cookielib.CookieJar()
opener = urllib2.build_opener(httpHandler, httpsHandler, urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

url = 'http://127.0.0.1:8069/web/login'
params = {
    'db': 'pms_db',
    'login': 'admin',
    'password': 'Password01!',
    'redirect': 'http://127.0.0.1:8069/web?db=pms_db',
}
content_type = 'application/x-www-form-urlencoded'
req = urllib2.Request(url)
body = urllib.urlencode(params)
req.add_data(body)
# req.add_data(file.read())
up_pic_header_built(req, body, content_type)
print body
response = urllib2.urlopen(req, timeout=20)

for index, cookie in enumerate(cj):
    print '[', index, ']', cookie
    # cookies = 'last_used_database=pufa_db;'

res_html = gzip_built(response)
print '%s' % res_html


# content_type = 'application/x-www-form-urlencoded'
req = urllib2.Request('http://127.0.0.1:8069/web?db=pms_db#page=0&limit=80&view_type=list&model=ir.attachment&menu_id=107&action=89')
# body = urllib.urlencode(params)
# req.add_data(body)
# req.add_data(file.read())
up_pic_header_built(req, None, None)
# print body
response = urllib2.urlopen(req, timeout=20)

for index, cookie in enumerate(cj):
    print '[', index, ']', cookie
    # cookies = 'last_used_database=pufa_db;'

res_html = gzip_built(response)
print '%s' % res_html