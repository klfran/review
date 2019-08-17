"""
httpserver 3.0
获取http请求
解析http请求
将请求发送给WebFrame
从WebFrame接收反馈数据
将数据组织为Response格式发送给客户端
"""
from socket import  *
import sys
from threading import  Thread
import  json,re
from config import  *
#import  time

#负责和webframe交互
def connect_frame(env):
    s = socket()
    try:
        s.connect((frame_ip,frame_port))
    except Exception as e:
        print(e)
        return
    data = json.dumps(env)
    s.send(data.encode())
    data = s.recv(1024*1024*10).decode()
    # timesleep(n,env)
    return json.loads(data)
#开启一个线程，每隔20s，执行一次心跳
# def timesleep(n,env):
#     for i in range(n):
#         time.sleep(20)
#         connect_frame(env)
# thread = Thread(target =timesleep,args = (3600*24,))
# thread.start()
#HTTPServer功能类
class HTTPServer:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.create_sockfd()
        self.bind()

    def create_sockfd(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,
                               DEBUG)

    def bind(self):
        self.address = (self.host,self.port)
        self.sockfd.bind(self.address)
    #启动服务
    def serve_forever(self):
        self.sockfd.listen(5)
        print("Start the httpserver : %d"%self.port)
        while True:
            connfd,addr = self.sockfd.accept()
            client = Thread(target = self.handle,args =(connfd,))
            client.setDaemon(True)
            client.start()
    #具体处理客户端请求
    def handle(self,connfd):
        request = connfd.recv(4096).decode()
        pattern = r'(?P<method>[A-Z]+)\s(?P<info>/\S*)'
        try:
            env = re.match(pattern,request).groupdict()
        except:
            connfd.close()
            return
        else:
            data = connect_frame(env)
            if data:
                self.response(connfd,data)

    def response(self,connfd,data):
        if data['status']  == '200':
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += "Content-Type:text/html\r\n"
            responseHeaders += "\r\n"
            responseBody = data['data']
        elif data['status'] == '404':
            responseHeaders = "HTTP/1.1 404 Not Found\r\n"
            responseHeaders += "Content-type:text/html\r\n"
            responseHeaders += "\r\n"
            responseBody = data['data']
        elif data['status'] == '302':
            pass
        data = responseHeaders + responseBody
        connfd.send(data.encode())


if __name__ == "__main__":
    httpd = HTTPServer()
    httpd.serve_forever()