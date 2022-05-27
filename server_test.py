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
import os
from socket import *
import threading

HOST = 'localhost' # Server IP
PORT = 9008 # PORT

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)         # 맵핑된 소켓을 연결 요청 대기 상태로 전환

print("서버 대기중(listen(1))")

while True:
    try:
        connectionSocket, addr = server_socket.accept() # 실제 소켓 연결 시 반환되는 실제 통신용 연결된 소켓과 연결 주소 할당

        if connectionSocket == -1:
            continue
        else:
            print(str(addr), "에서 접속되었습니다.")  # 연결 완료 프린트문

        pid = os.fork()
        if pid == -1:
            connectionSocket.close()
            print('pid: {}\tconnectionSocket.close()'.format(pid))
            continue
        elif pid == 0:
            server_socket.close()
            print('pid: {}\tserver_socket.close()'.format(pid))
            while True:
                recvData = connectionSocket.recv(1024)
                data = str(recvData.decode("UTF-8"))
                print("받은 데이터: ", data)  # 받은 데이터 UTF-8

                sendData = data
                try:
                    connectionSocket.send(sendData.encode("UTF-8"))  # 데이터 송신
                    print("데이터 전송: ", sendData)
                except error as e:
                    print('전송 에러: ', e)

                if data == 'exit':
                    break

            connectionSocket.close()
            print(str(addr), '접속 종료')

        else:
            connectionSocket.close()
            print('pid: {}\tconnectionSocket.close()'.format(pid))

    except error as e:
        print("error: ", e)
        break

server_socket.close() # 서버 종료