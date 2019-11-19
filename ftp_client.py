"""
ftp 文件服务 客户端
"""
from socket import *
import sys
from time import sleep

# 服务器地址
ADDR = ('127.0.0.1',8080)

# 实现客户端发送请求的方法
class FTPClient:
    def __init__(self,sockfd):
        self.sockfd = sockfd

    # 获取文件列表
    def do_list(self):
        self.sockfd.send(b'LIST') # 发送请求
        # 等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            # 一次性接收所有文件形参的大字符串
            data = self.sockfd.recv(1024 * 1024)
            print(data.decode())
        else:
            print(data) # 不成功原因

    # 下载文件
    def do_get(self,filename):
        # 发送请求
        self.sockfd.send(('GET ' + filename).encode())
        # 等待反馈
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            f = open(filename,'wb')
            while True:
                # 边收取内容,边写入文件
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break # 文件发送完毕
                f.write(data)
            f.close()
        else:
            print(data)

    # 上传文件
    def do_put(self,filename):
        try:
            f = open(filename,'rb')
        except Exception:
            print("该文件不存在")
            return
        # 发送请求
        filename = filename.split('/')[-1] # 提取文件名称
        self.sockfd.send(('PUT '+filename).encode())
        # 接收反馈
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            while True:
                data = f.read(1024)
                if not data:
                    sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print(data)

# 网络搭建 (和服务端建立通信,然后通过打印命令提示选择执行的功能)
def main():
    sockfd = socket()
    sockfd.connect(ADDR)

    ftp = FTPClient(sockfd) # 实例化对象用来调用方法

    # 循环发送请求
    while True:
        print("""\n=========Command===========
***        list       ***
***     get  file     ***
***     put  file     ***
***        exit       ***
===========================""")
        cmd = input("输入命令:")
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd[:4] == 'get ':
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:4] == 'put ':
            filename = cmd.split(' ')[-1]
            ftp.do_put(filename)
        elif cmd == 'exit':
            sockfd.send(cmd.encode())
        else:
            print("请输入正确命令")

if __name__ == '__main__':
    main()














