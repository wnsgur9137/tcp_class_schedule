from socket import *
import threading


def read_send(fileName):
    fileContent = ''
    with open(fileName) as fp:
        lines = fp.readlines()
        for line in lines:
            print(line[:-1])
            fileContent += line[:-1]

        connectionSocket.send(fileContent.encode("UTF-8"))

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

    connect = True
    # while connect:
    for _ in range(5):
        connectionSocket, addr = server_socket.accept()  # 실제 소켓 연결 시 반환되는 실제 통신용 연결된 소켓과 연결 주소 할당
        print(str(addr), "에서 접속되었습니다.")  # 연결 완료 프린트문
        while connect:
            recvData = connectionSocket.recv(1024)  # 데이터 수신 최대 1024byte
            data = str(recvData.decode("UTF-8"))
            print("받은 데이터: ", data)  # 받은 데이터 UTF-8

            fileName = './resorces/'
            if data == '1':
                fileName += '1_subject.txt'
                read_send(fileName)
            elif data == '2':
                fileName += '2_subject.txt'
                read_send(fileName)
            elif data == '3':
                fileName += '3_subject.txt'
                read_send(fileName)
            elif data == '4':
                print('4')
                connectionSocket.send('ERROR'.encode("UTF-8"))
            elif data == 'exit':
                break
            else:
                print("ERROR")
                connectionSocket.send('ERROR'.encode("UTF-8"))

            # connectionSocket.sendall(fileContent.encode("UTF-8"))
            # connectionSocket.send("I am a server ".encode("UTF-8"))  # 데이터 송신
            print("데이터 전송")

    server_socket.close()  # 서버 종료
