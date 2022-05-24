# server_test v01

# import socket
#
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(('localhost', 9008))
# server_socket.listen(0) # 클라이언트의 연결요청을 기다리는 상태
#
# client_socket, addr = server_socket.accept() # 연결 요청 수락 -> IP/PORT return
#
# data = client_socket.recv(65535) # 클라이언트로부터 데이터를 받는다. (출력되는 버퍼 사이즈)
#
# print("받은 데이터:", data.decode()) # 받은 데이터 해석


from socket import *
import threading

HOST = 'localhost' # Server IP
PORT = 9008 # PORT

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)         # 맵핑된 소켓을 연결 요청 대기 상태로 전환

print("서버 대기중(listen(1))")

connectionSocket, addr = server_socket.accept() # 실제 소켓 연결 시 반환되는 실제 통신용 연결된 소켓과 연결 주소 할당

print(str(addr), "에서 접속되었습니다.") # 연결 완료 프린트문

data = connectionSocket.recv(1024) # 데이터 수신 최대 1024byte

print("받은 데이터: ", data.decode("utf-8")) # 받은 데이터 UTF-8

connectionSocket.send("I am a server".encode("UTF-8")) # 데이터 송신
print("데이터 전송")

server_socket.close() # 서버 종료