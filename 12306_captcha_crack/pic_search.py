#encoding=utf-8
import os
import urllib
import urllib2
import cookielib
import poster
import zlib
from bs4 import BeautifulSoup
import re
from PIL import Image
import StringIO


def up_pic_header_built(req):
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Cache-Control', 'no-cache')
    req.add_header('Connection', 'Keep-Alive')
    req.add_header('Content-Type', 'image/jpeg')
    req.add_header('Pragma', 'no-cache')
    req.add_header('Referer', 'http://shitu.baidu.com/')
    req.add_header('User-Agent', 'fake-client')


def search_pic_header_built(req):
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Encoding', 'gzip, deflate, sdch')
    req.add_header('Connection', 'Keep-Alive')
    req.add_header('User-Agent', 'fake-client')


def gzip_built(response):
    res_html = response.read()
    # print res_html
    if response.info().get('Content-Encoding') == 'gzip':
        res_html = zlib.decompress(res_html, 16+zlib.MAX_WBITS)
        # print res_html
    return res_html


def find_info(res_html):
    res = []
    re_1 = re.compile(u'escapeXSS\("[\w+|\u4e00-\u9fa5|*]+')
    re_2 = re.compile(u'[\u4e00-\u9fa5]+')
    re_str_1 = re_1.findall(res_html.decode('utf-8'))
    if re_str_1:
        re_str_2 = re_str_1[0].split('"')
        if len(re_str_2) > 1:
            res = re_2.findall(re_str_2[1])

    print u'图片识别关键字:%s' % str(res)
    return res

def findall_info(res_html):
    res = []
    re_1 = re.compile(u'[\u4e00-\u9fa5]{1,8}')
    res = re_1.findall(res_html.decode('utf-8'))
    print u'图片识别关键字:%s' % str(res)
    return res


def get_pic_info(type='file', file=None):
    """
    #debug日志
    httpHandler = urllib2.HTTPHandler(debuglevel=1)
    httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(httpHandler, httpsHandler, urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    """
    #cookie
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    #百度 图片上传API
    url = 'http://shitu.baidu.com/n/image?\
fr=html5&\
needRawImageUrl=true&\
id=WU_FILE_0&\
name=%E7%AB%99%E7%82%B9.jpg&\
type=image%2Fjpeg&\
lastModifiedDate=Thu+Dec+18+2014+13%3A26%3A15+GMT%2B0800+(CST)&\
size=16717'
    #百度 图片搜索API
    api_1 = 'http://stu.baidu.com/i?objurl=%s\
&filename=&rt=0&rn=10&ftn=searchstu&ct=1&stt=1&tn=faceresult'
    api_2 = 'http://stu.baidu.com/i?ct=3&tn=shituresult&pn=0&rn=10&querysign=3046724883,3054654929&shituRetNum=8&similarRetNum=600&faceRetNum=1000&setnum=0&beautynum=0'
    api_3 = 'http://stu.baidu.com/i?ct=3&tn=facejson&rn=6&querysign=3544027739,3922013179&shituRetNum=8&similarRetNum=20&faceRetNum=10&setnum=0&beautynum=0&stt=1&size_filter=-1&tab=0&pn=0&date_filter=0&width=&height=&ic=0&z=&sign=3046724883,3054654929'

    # params = {
    #     'file': file,
    # }

    req = urllib2.Request(url)
    # req.add_data(urllib.urlencode(params))
    req.add_data(file.read())
    up_pic_header_built(req)

    response = urllib2.urlopen(req, timeout=20)
    res_html = gzip_built(response)
    print u'图片上传成功:%s' % res_html

    # cookie
    # for index, cookie in enumerate(cj):
    #     print '[', index, ']', cookie

    pic_url = api_1 % res_html
    pic_req = urllib2.Request(pic_url)
    search_pic_header_built(pic_req)
    pic_response = urllib2.urlopen(pic_req, timeout=20)
    res_html = gzip_built(pic_response)
    info_list = find_info(res_html)
    # info_list = findall_info(res_html)

    return info_list


if __name__ == '__main__':
    print u'图片验证开始'

    #获取12306验证码 (暂使用本地图片)
    image_12306 = Image.open("image/12306_1.jpg")

    #分割验证码
    regions = [
        # (0, 0, 293, 190),
        #文字
        {'type': 'name', 'region': (120, 1, 182, 29)},
        #8个图片
        {'type': 'image', 'region': (3, 40, 74, 110)},
        {'type': 'image', 'region': (74, 40, 145, 110)},
        {'type': 'image', 'region': (145, 40, 217, 110)},
        {'type': 'image', 'region': (217, 40, 288, 110)},
        {'type': 'image', 'region': (3, 110, 74, 180)},
        {'type': 'image', 'region': (74, 110, 145, 180)},
        {'type': 'image', 'region': (145, 110, 217, 180)},
        {'type': 'image', 'region': (217, 110, 288, 180)},
    ]
    title_image = u'煤'
    crop_images = []
    num = 1
    for region in regions:
        if region['type'] == 'image':
            crop_image = image_12306.crop(region['region'])
            crop_images.append(crop_image)
            # crop_image.save('image/12306_1_%s.jpg' % num)
            num += 1
        elif region['type'] == 'name':
            pass

    #文字验证

    #图片验证
    info_list = []
    for crop_image in crop_images:
        file = StringIO.StringIO()
        crop_image.save(file, "JPEG")
        file.seek(0)

        # file = open("image/站点.jpg", "rb")
        pic_info_list = get_pic_info(type='file', file=file)
        info_list.append(pic_info_list)

    #验证完成后操作
    print u'图片验证顺序:自左向右，自上向下。'
    num = 1
    for info in info_list:
        if info and title_image in ','.join(info):
            print u'图片%s验证成功!' % (num)
        else:
            print u'图片%s验证失败!' % (num)
        num += 1

    print u'图片验证结束'




