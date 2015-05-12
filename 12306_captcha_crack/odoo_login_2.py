# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    # filename='migratio.log',
    filemode='w',
)
# 日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
import base64
import json
import urllib
import re
import requests
#sudo apt-get install scons libboost-python-dev  pyv8依赖库
# import PyV8
from imapclient import IMAPClient
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate
from email import encoders
from xml.etree import ElementTree
from sqlalchemy import create_engine

res = {
    'login': {},
    'start': {},
    'select': {},
}
res['login']['headers'] = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Referer': 'http://127.0.0.1:8069/web/login?redirect=http%3A%2F%2F127.0.0.1%3A8069%2Fweb%3Fdb%3Dpms_db',
    'User-Agent': 'fake-client',
}
res['login']['data'] = {
    'db': 'pms_db',
    'login': 'admin',
    'password': 'Password01!',
    'redirect': 'http://127.0.0.1:8069/web?db=pms_db',
}
login_url = 'http://127.0.0.1:8069/web/login'

res['start']['headers'] = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Referer': 'http://127.0.0.1:8069/',
    'User-Agent': 'fake-client',
}
start_url = 'http://127.0.0.1:8069/web'

res['select']['headers'] = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Referer': 'http://127.0.0.1:8069/web?db=pms_db',
    'User-Agent': 'fake-client',
}
select_url = 'http://127.0.0.1:8069/web/login?redirect=http%3A%2F%2F127.0.0.1%3A8069%2Fweb%3Fdb%3Dpms_db'

req_down = requests.Session()

response = req_down.get(start_url,
                    headers=res['start']['headers'],
                    timeout=5,
                    allow_redirects=True)

if response.status_code in [200]:
    pass

response = req_down.get(select_url,
                    headers=res['select']['headers'],
                    timeout=5,
                    allow_redirects=True)

if response.status_code in [200]:
    pass

response = req_down.post(login_url,
                    data=urllib.urlencode(res['login']['data']),
                    headers=res['login']['headers'],
                    timeout=5,
                    allow_redirects=True)

if response.status_code in [200]:
    pass