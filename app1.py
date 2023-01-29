import socket
import sys
import os
import time


def main():
    # 1. 创建套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2. 绑定本地信息
    if sys.argv.__len__() == 2:
        port = int(sys.argv[1])
        print('server listening on port: %d' % port)
    else:
        print('请使用python xxx.py 8888的方式调用')
        return

    server_socket.bind(("", port))
    # 3. 变为监听套接字
    server_socket.listen(128)
    # 4. 等待对方连接
    while True:
        client_socket, addr = server_socket.accept()

        # 接收数据
        request = client_socket.recv(1024).decode('utf-8')
        file_name = request.splitlines()[0].split()[1]
        if file_name == '/':
            file_name = '/index.html'
        file_name = './html' + file_name

        response_header = "HTTP/1.1 200 OK\r\n"
        response_header += "\r\n"
        client_socket.send(response_header.encode('utf-8'))

        if os.path.exists(file_name):
            f = open(file_name, 'rb')
            content = f.read()
            client_socket.send(content)
            time.sleep(2)
            f.close()

        client_socket.close()


if __name__ == '__main__':
    main()
