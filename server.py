from socket import *
import os
import threading


def read_send(fileName):
    file = './resorces/'+fileName+'.txt'
    print('file: ', file)
    try:
        fileContent = ''
        with open(file) as fp:
            lines = fp.readlines()
            for line in lines:
                print(line[:-1])
                fileContent += line[:-1]

            connectionSocket.send(fileContent.encode("UTF-8"))
            print("데이터 전송", file, str(addr))
    except error as e:
        print("[ERROR]\t", e)
        connectionSocket.send("ERROR".encode("UTF-8"))
        pass

    # try:
    #     data = fp.read(1024)
    #     while data:
    #         data_transferred += connectionSocket.send(data)
    #         data = fp.read(1024)
    # except Exception as ex:
    #     print(ex)


if __name__ == '__main__':
    HOST = 'localhost'  # Server IP
    PORT = 9008  # PORT

    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    server_socket.listen(1)  # 맵핑된 소켓을 연결 요청 대기 상태로 전환
    print("서버 대기중(listen(1))")

    while True:
        try:
            connectionSocket, addr = server_socket.accept()  # 실제 소켓 연결 시 반환되는 실제 통신용 연결된 소켓과 연결 주소 할당

            if connectionSocket == -1:
                continue
            else:
                print(str(addr), "에서 접속되었습니다.")  # 연결 완료 프린트문

            pid = os.fork()
            if pid == -1:
                connectionSocket.close()
                print('connectionSocket.close() # if')
                continue
            elif pid == 0:
                server_socket.close()
                print('server_socket.close()')
                while True:
                    recvData = connectionSocket.recv(1024)  # 데이터 수신 최대 1024byte
                    data = str(recvData.decode("UTF-8"))
                    print("받은 데이터: ", data, str(addr))  # 받은 데이터 UTF-8
                    try:
                        if data == 'exit':
                            break
                        else:
                            read_send(data)
                    except:
                        connectionSocket.send("ERROR".encode("UTF-8"))

                connectionSocket.close()
                print(str(addr), '접속이 종료되었습니다.')
                exit()
            else:
                connectionSocket.close()
        except error as e:
            print("오류", e)
            pass

    print('server 종료')
    server_socket.close()
