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


def up_pic_header_built(req, body, content_type=None):
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Connection', 'Keep-Alive')
    req.add_header('Origin', 'http://127.0.0.1:8069')
    req.add_header('Referer', 'http://127.0.0.1:8069/web?db=pms_db')
    req.add_header('User-Agent', 'fake-client')
    if content_type:
        req.add_header('Content-Type', content_type)
    req.add_header('Content-Length', str(len(body)))

def gzip_built(response):
    res_html = response.read()
    # print res_html
    if response.info().get('Content-Encoding') == 'gzip':
        res_html = zlib.decompress(res_html, 16+zlib.MAX_WBITS)
        # print res_html
    return res_html

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = mimetools.choose_boundary()
    # BOUNDARY = '175056440752918429230479495'
    # BOUNDARY = '----WebKitFormBoundaryKvH0d5ngLRqLIBLT'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

#debug日志
httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
cj = cookielib.CookieJar()
opener = urllib2.build_opener(httpHandler, httpsHandler, urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

url = 'http://127.0.0.1:8069/web/binary/upload_attachment/'
params = [
    ('callback', 'oe_fileupload_temp37'),
    ('model', 'yins.ipm.contract'),
    ('id', '0'),
    ('file_res', '{"labels": []}'),
]
file = open("image/站点.jpg", "rb")
files = [
    ('ufile', file.name, file.read())
]
content_type, body = encode_multipart_formdata(params, files)

req = urllib2.Request(url)
req.add_data(body)
# req.add_data(file.read())
up_pic_header_built(req, body, content_type)
print body
response = urllib2.urlopen(req, timeout=20)
res_html = gzip_built(response)
print u'附件上传成功:%s' % res_html
