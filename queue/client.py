#coding=utf-8
import socket
import time

if __name__ == '__main__':
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    conn = '/tmp/conn'
    sock.connect(conn)
    time.sleep(1)
    sock.send('请求队列:%s' % '')
    print sock.recv(1024)
    sock.close()
    print '结束'