# client_test v01

# import socket
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# sock.connect(("localhost", 9008))
# sock.send('Hello'.encode())

from socket import *

IP = 'localhost'
PORT = 9008

# client_socket = socket.socket(socket.AF_INET, SOCK_STREAM)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((IP, PORT))
print("연결 확인")

client_socket.send("I am a client".encode("UTF-8")) # 데이터 송신
print("데이터 전송")

data = client_socket.recv(1024) # 데이터 수신
print("데이터 수신 받은 데이터: ", data.decode("UTF-8"))
client_socket.close()