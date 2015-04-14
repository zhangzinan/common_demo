#-*-coding:UTF-8-*-
import socket
#import thread
import select
from urlparse import urlparse

class Restful:
    def __init__(self,ip='127.0.0.1',port=12345):
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server.bind((ip,port))
        self.server.listen(1)
        self.client=None
        self.uri=None
        self.path=None
        self.method=None
        self.body=None
        self.header=None
        self.resourceMethod=[]
        self.urlparser=None
        self.rest={}
    def router(self,uri,method='GET'):  #这里使用了一点技巧
        self.uri=uri
        self.resourceMethod.append(method)
        def _rout(func):
            self.rest[uri]=func
        return _rout
    def getClientInfo(self):
        self.client,_=self.server.accept()
        data=self.client.recv(4096)
       
        tmp=data.split('\r\n')
        firstLine=tmp[0]
        firstLine=firstLine.split()
        self.method=firstLine[0]
        self.path=firstLine[1]
        self.urlparser=urlparse(self.path)
        l=len(tmp)
        self.header=tmp[1:l-2]
        self.body=tmp[l-1]
       
        res=self.__getKey()
        if  res is None:
            print 'Url no match'
            self.client.close()
            return None
        print '-->',self.uri
        if 'GET'==self.__isMethod('GET'):
            self.do_GET()
        elif 'POST' ==self.__isMethod('POST'):
            self.do_POST()
        elif 'DELETE' == self.__isMethod('DELETE'):
            self.do_DELETE()
        elif 'PUT' == self.__isMethod('PUT'):
            self.do_PUT()
    def getAttribute(self,attr):   #上面介绍的getAttribute()函数在这儿
        attrs=self.urlparser.path.split('/')
        formatAttrs=self.uri.split('/')
        for i in range(len(attrs)):
            if attr in formatAttrs[i]:
                return attrs[i]
        return ''
    def query(self,param):         #上面介绍的query()函数在这儿
        vals=self.urlparser.query.split('&')
        if 'POST' == self.__isMethod('POST'):
            postvals=self.body.split('&')
            vals+=postvals
        res=None
        for v in vals:
            if param in v:
                if '=' in v:
                    res= v.split('=')[1]
                else:
                    res= True
        if res:
            return res
        else:
            return None
    def __isMethod(self,m):
        if m==self.method and m in self.resourceMethod:
            return m
        else:
            return None
    def __getKey(self):
        for k in self.rest.keys():
            c=k.find('[')
            ktmp=k[:c]
            if ktmp in self.urlparser.path:
                self.uri=k
                break
        if self.uri:
            return True
        return None
    def do_GET(self):
        src=self.rest[self.uri]()
        self.blocking(src)
    def do_POST(self):
        src=self.rest[self.uri]()
        self.blocking(src)
    def do_DELETE(self):
        src=self.rest[self.uri]()
        self.blocking(src)
    def do_PUT(self):
        src=self.rest[self.uri]()
        self.blocking(src)
    def run(self):
        while True:
            self.getClientInfo()
    def blocking(self,sendInfo):
        response='HTTP/1.1 200 OK\r\n'+ \
            'Content-type: text/html\r\n\r\n'
        sendInfo=response+sendInfo+'\r\n'
        self.client.send(sendInfo)
        self.client.close()

#------------Test------------------ #这里是测试部分也是例子
rest=Restful()
@rest.router('/wm/[a]?')            #例子1,router()第二个参数默认是GET方法
def test():
    a=rest.getAttribute('a')
    v=rest.query('u')
    if not v:
        v=''
    elif v is True:
        v='\"true\"'
    return '{\"test\":'+a+',\"value\":'+v+'}'

@rest.router('/vpc/[b]')            #例子2
def test():
    attrB=rest.getAttribute('b')
    return '{\"vpc\":'+attrB+'}'

@rest.router('/post','POST')        #例子3,这里router（）第二个参数是POST
def testPost():
    p=rest.query('p') or ''
    v=rest.query('v') or ''
    return '{\"q\":'+p+',\"v\":'+v+'}'
rest.run()

# http://127.0.0.1:12345/wm/1?u=12
# http://127.0.0.1:12345/post?p=12&v=12