import socket
import threading

hostport = ('192.168.0.174', 9999)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(hostport)
true = True


def Receve(s):
    global true
    while true:
        data = s.recv(1024).decode('utf8')
        if data == 'quit' or data is None:
            true = False
        print(data)


thrd = threading.Thread(target=Receve, args=(s,))
thrd.start()
while true:
    user_input = input()
    s.send(user_input.encode('utf8'))
    if user_input == 'quit':
        true = False
