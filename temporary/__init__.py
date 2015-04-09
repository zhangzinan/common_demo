#coding=utf=8
import os
import mimetypes


path = '/home/openerp/图片/20131111-4（1）.jpg'
file = open(path, 'rb')
ctype, encoding = mimetypes.guess_type(path)
pass