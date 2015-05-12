#coding=utf-8
import socket
import os

if __name__ == '__main__':
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    conn = '/tmp/conn'
    if not os.path.exists(conn):
        os.mknod(conn)
    if os.path.exists(conn):
        os.unlink(conn)
        sock.bind(conn)
        sock.listen(5)
    while True:
        connection, address = sock.accept()
        data = connection.recv(1024)
        print "接受到数据为:%s!\n" % data
        connection.send("处理成功!")
        connection.close()