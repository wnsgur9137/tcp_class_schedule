from socket import *    # socket 라이브러리
import os               # fork() 함수를 사용하기 위한 라이브러리
import threading        # thread 사용을 위한 라이브러리
import weather_api      # 날씨 api를 사용하는 py파일
import schedule         # 정해진 시간마다 날씨 api를 업데이트하기 위함
import time           # time.sleep() 사용 위한 라이브러리


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


def send_weather():
    weather_data_dict = weather_api.get_today_weather()
    weather_data_key = list(weather_data_dict.keys())
    weather_data_value = list(weather_data_dict.values())
    if weather_data_value[0] == '0':
        weather_data_value[0] = '없음'
    elif weather_data_value[0] == '1':
        weather_data_value[0] = '비'
    elif weather_data_value[0] == '2':
        weather_data_value[0] = '비/눈'
    elif weather_data_value[0] == '3':
        weather_data_value[0] = '눈'
    elif weather_data_value[0] == '5':
        weather_data_value[0] = '빗방울'
    elif weather_data_value[0] == '6':
        weather_data_value[0] = '빗방울/눈 날림'
    elif weather_data_value[0] == '7':
        weather_data_value[0] = '눈날림'

    if weather_data_value[2] == '1':
        weather_data_value[2] = '맑음'
    elif weather_data_value[2] == '2':
        weather_data_value[2] = '구름조금'
    elif weather_data_value[2] == '3':
        weather_data_value[2] = '구름많음'
    elif weather_data_value[2] == '4':
        weather_data_value[2] = '흐림'

    if weather_data_value[1] != '강수없음':
        weather_data_value[1] += 'mm'

    weather_data_str = ''
    for i in range(len(weather_data_key)):
        weather_data_str += weather_data_key[i] + ':'
        weather_data_str += weather_data_value[i] + ','
        # weather_data_list.append(weather_data_key[i])
        # weather_data_list.append(weather_data_value[i])

    connectionSocket.send(weather_data_str.encode("UTF-8"))


def weather_update():   #schedule 라이브러리 사용한 정기적인 업데이트
    global weather_data
    weather_data = weather_api.get_today_weather()
    print('\n[weather 정기 업데이트]\n')


weather_data = {}


if __name__ == '__main__':
    HOST = 'localhost'  # Server IP
    PORT = 9008  # PORT

    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    server_socket.listen(1)  # 맵핑된 소켓을 연결 요청 대기 상태로 전환
    print("서버 가동중")

    weather_data = weather_api.get_today_weather()
    schedule.every().minute.at(':50').do(weather_update)
    print("서버 가동 완료... 접속 대기중")
    while True:
        schedule.run_pending()
        time.sleep(10)
        try:
            connectionSocket, addr = server_socket.accept()  # 실제 소켓 연결 시 반환되는 실제 통신용 연결된 소켓과 연결 주소 할당

            if connectionSocket == -1:
                continue
            else:
                print(str(addr), "에서 접속되었습니다.")  # 연결 완료 프린트문

            pid = os.fork()
            if pid == -1:
                connectionSocket.close()
                continue
            elif pid == 0:
                server_socket.close()
                while True:
                    recvData = connectionSocket.recv(1024)  # 데이터 수신 최대 1024byte
                    data = str(recvData.decode("UTF-8"))
                    print("받은 데이터: ", data, str(addr))  # 받은 데이터 UTF-8
                    try:
                        if data == 'exit':
                            break
                        elif data == 'weather':
                            send_weather()
                        else:
                            read_send(data)
                    except error as e:
                        print(e)
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
