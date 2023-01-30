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

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    # 3. 变为监听套接字
    server_socket.listen(128)
    # 4. 等待对方连接
    while True:
        client_socket, addr = server_socket.accept()

        # 接收数据
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            continue
        file_name = request.splitlines()[0].split()[1]
        if file_name == '/':
            file_name = '/index.html'
        file_name = './html' + file_name

        if os.path.exists(file_name):
            try:
                f = open(file_name, 'rb')
            except:
                response_header = "HTTP/1.1 404 not found\r\n\r\n"
                response_body = "file not found."
                client_socket.send(response_header.encode('utf-8'))
                client_socket.send(response_body.encode('utf-8'))
            else:
                content = f.read()
                response_header = "HTTP/1.1 200 OK\r\n\r\n"
                client_socket.send(response_header.encode('utf-8'))
                client_socket.send(content)
                time.sleep(1)
                f.close()
            finally:
                client_socket.close()
        else:
            response_header = "HTTP/1.1 404 not found\r\n\r\n"
            response_body = "file not found."
            client_socket.send(response_header.encode('utf-8'))
            client_socket.send(response_body.encode('utf-8'))
            client_socket.close()


if __name__ == '__main__':
    main()
