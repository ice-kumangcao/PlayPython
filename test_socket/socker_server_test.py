import socket
import threading

HOST = '192.168.0.174'
PORT = 9999

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen()
socket_list = []


def receive(connection: socket.socket, address, run_flag):
    while run_flag:
        data = connection.recv(1024).decode('utf-8')
        if data == 'quit' or data is None or data == '':
            run_flag = False
        print(address, ":", data)
        for a_socket in socket_list:
            if a_socket == connection:
                continue
            try:
                if a_socket is not None and not a_socket._closed:
                    content = address + ': ' + data
                    a_socket.send(content.encode('utf-8'))
            except Exception as e:
                print(e)
                a_socket.close()


while True:
    connection, address = serverSocket.accept()
    address = str(address)
    socket_list.append(connection)
    run_flag = True
    receive_thread = threading.Thread(target=receive, args=(connection, address, run_flag,))
    receive_thread.start()
