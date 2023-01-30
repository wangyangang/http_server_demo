import socket
import sys
import os
import time


class WSGIServer:
    def __init__(self, port, document_root):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("", port))
        # 3. 变为监听套接字
        self.server_socket.listen(128)

        self.document_root = document_root

    def run_forever(self):
        while True:
            self.client_socket, addr = self.server_socket.accept()
            self.handle_request()

    def handle_request(self):
        request = self.client_socket.recv(1024).decode('utf-8')
        if not request:
            return

        file_name = request.splitlines()[0].split()[1]
        if file_name == '/':
            file_name = '/index.html'
        file_name = self.document_root + file_name

        if os.path.exists(file_name):
            try:
                f = open(file_name, 'rb')
            except:
                response_header = "HTTP/1.1 404 not found\r\n\r\n"
                response_body = "file not found."
                self.client_socket.send(response_header.encode('utf-8'))
                self.client_socket.send(response_body.encode('utf-8'))
            else:
                content = f.read()
                response_header = "HTTP/1.1 200 OK\r\n\r\n"
                self.client_socket.send(response_header.encode('utf-8'))
                self.client_socket.send(content)
                time.sleep(1)
                f.close()
            finally:
                self.client_socket.close()
        else:
            response_header = "HTTP/1.1 404 not found\r\n\r\n"
            response_body = "file not found."
            self.client_socket.send(response_header.encode('utf-8'))
            self.client_socket.send(response_body.encode('utf-8'))
            self.client_socket.close()


def main():
    if sys.argv.__len__() == 2:
        port = int(sys.argv[1])
        print('server listening on port: %d' % port)
    else:
        print('请使用python xxx.py 8888的方式调用')
        return

    http_server = WSGIServer(port, "./html")
    http_server.run_forever()


if __name__ == '__main__':
    main()