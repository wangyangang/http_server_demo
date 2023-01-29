import socket


def main():
    # 1. 创建套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2. 绑定本地信息
    server_socket.bind(("", 9999))
    # 3. 变为监听套接字
    server_socket.listen(128)
    # 4. 等待对方连接
    while True:
        client_socket, addr = server_socket.accept()

        # 接收数据
        client_socket.recv(1024)

        response_header = "HTTP/1.1 200 OK\r\n"
        response_header += "\r\n"
        response_body = "hello"

        response = response_header + response_body

        client_socket.send(response.encode("UTF-8"))
        client_socket.close()


if __name__ == '__main__':
    main()
