import socket
from socket import *
from _thread import *
import threading
import os
import weather_api
import schedule
import time


def read_send(filename, client_socket_thread, addr_thread):
    """
    .txt 파일 읽고 전송
    """
    file = './resources/'+filename+'.txt'
    print('file: ', file)

    fileContent = str() # 클라이언트 측에 전송하기 위한(인코딩 하기 위한) 문자열 형태의 전송 형식
    lock.acquire()  # 파일을 읽어올 때 뮤텍스(thread lock)을 걸어준다.
    try:
        with open(file) as fp:
            lines = fp.readlines()
            for line in lines:
                print(line[:-1])
                fileContent += line[:-1]    # .txt 파일의 한 라인씩 fileContent 문자열에 추가한다.

            client_socket_thread.send(fileContent.encode("UTF-8"))  # 클라이언트 측에 fileContent 문자열을 전송한다.
            print('데이터 전송', file, str(addr_thread))
    except error as e:
        print('ERROR', e)   # 전송 중 에러가 발생할 경우, ERROR 메세지를 클라이언트 측에 전송한다.
        client_socket_thread.send('ERROR: read_send()'.encode("UTF-8"))
    finally:
        lock.release() # try/except 문이 종료되면 뮤텍스(thread lock)을 해제한다.


def send_weather(client_socket_thread, addr_thread):
    """
    현재 날씨 전송
    """
    lock.acquire()  # 뮤텍스(Lock)
    weather_data_key = list(weather_data_dict.keys())
    weather_data_value = list(weather_data_dict.values())
    lock.release()  # 뮤텍스(Lock)

    weather_data_str = str()
    for i in range(len(weather_data_key)):  # 클라이언트에 전송하기 위해 문자열로 변경.
        weather_data_str += weather_data_key[i] + ':'
        weather_data_str += weather_data_value[i] + ','

    print('\n\nweather_data_str')
    print(weather_data_str)

    lock.acquire()  # 뮤텍스(Lock)
    client_socket_thread.send(weather_data_str.encode("UTF-8"))
    print('데이터 전송', weather_data_dict, str(addr_thread))
    lock.release()  # 뮤텍스(Lock)


def weather_update():
    """
    날씨 정기 업데이트
    """
    global weather_data_dict

    lock.acquire()  # 뮤텍스(Lock)
    print('\n\n[날씨 정기 업데이트]')
    weather_data_dict = weather_api.get_today_weather()
    lock.release()  # 뮤텍스(Lock)


def schedule_thread():
    """
    주기적으로 날씨를 업데이트하는 함수(thread로 사용)
    매 시간 45분에 데이터가 업데이트 되므로,
    여유 있게 매 시간 50분에 실행
    """
    # schedule.every().minute.at(':50').do(weather_update) # 테스트 코드 (매 분 50초마다 작동)
    schedule.every().hour.at(':50').do(weather_update) # 매 시간 50분마다 동작
    while True:
        schedule.run_pending()
        time.sleep(30)  # 30초마다 한 번씩 시간이 시간이 일치하는지 확인한다.


def threaded(client_socket_thread, addr_thread):
    """
    스레드로 만든 각 클라이언트와 통신할 함수
    클라이언트가 종료되기 전까지 무한 루프
    """
    print(str(addr_thread), "thread.")
    while True:
        try:
            data = str(client_socket_thread.recv(1024).decode('UTF-8'))
            print('받은 데이터: ', data)
            if not data:
                print('받은 데이터가 없습니다.')
                break
            elif data == 'exit':
                break
            elif data == 'weather':
                send_weather(client_socket_thread, addr_thread)
            else :
                read_send(data, client_socket_thread, addr_thread)
        except ConnectionResetError as e:
            print('ConnectionResetError: ', e)
            # lock.acquire()
            client_socket_thread.send('ConnectionResetError: threaded()'.encode('UTF-8'))
            # lock.release()
        except error as e:
            print('ERROR: ', e)
            # lock.acquire()
            client_socket_thread.send('ERROR: threaded()'.encode('UTF-8'))
            # lock.release()
    client_socket_thread.close()
    print(str(addr_thread), '접속이 종료되었습니다.')


def run_accept_thread():
    """
    클라이언트 접속 대기상태
    """
    # server_socket.listen(1)  # 맵핑된 소켓을 연결 요청 대기 상태로 전환
    print('서버 가동 완료... ')
    while True:
        print("접속 대기중...")
        try:
            client_socket_thread, addr_thread = server_socket.accept()
            start_new_thread(threaded, (client_socket_thread, addr_thread, ))
        except error as e:
            print(e)


if __name__ == '__main__':
    IP = 'localhost'
    PORT = 9008

    lock = threading.Lock() # 뮤텍스(Lock)

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((IP, PORT))
    print("서버 가동중 ...\t IP: {0}, PORT: {1}".format(IP, PORT))

    weather_data_dict = weather_api.get_today_weather()
    weather_thread = threading.Thread(target=schedule_thread, daemon=True)  # 정기적인 날씨 업데이트
    weather_thread.start()

    server_socket.listen(1)  # 맵핑된 소켓을 연결 요청 대기 상태로 전환
    print('서버 가동 완료... ')
    while True:
        print("접속 대기중...")
        try:
            client_socket, addr = server_socket.accept()
            start_new_thread(threaded, (client_socket, addr,))
        except error as e:
            print(e)

    print('server 종료')
    server_socket.close()
