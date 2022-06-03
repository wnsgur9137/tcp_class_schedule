from socket import *
# from _thread import *
import threading
import os
import weather_api
import schedule
import time


def read_send(filename):
    """
    txt파일 읽고 전송
    """
    file = './resorces/'+filename+'.txt'
    print('file: ', file)

    fileContent = str()
    try:
        with open(file) as fp:
            lines = fp.readlines()
            for line in lines:
                print(line[:-1])
                fileContent += line[:-1]

            client_socket.send(fileContent.encode("UTF-8"))
            print('데이터 전송', file, str(addr))
    except error as e:
        print('ERROR', e)
        client_socket.send('ERROR: read_send()'.encode("UTF-8"))


def send_weather():
    """
    현재 날씨 전송
    """
    lock.acquire()
    weather_data_key = list(weather_data_dict.keys())
    weather_data_value = list(weather_data_dict.values())
    lock.release()

    weather_data_str = str()
    for i in range(len(weather_data_key)):
        weather_data_str += weather_data_key[i] + ':'
        weather_data_str += weather_data_value[i] + ','

    print('\n\nweather_data_str')
    print(weather_data_str)

    client_socket.send(weather_data_str.encode("UTF-8"))


def weather_update():
    """
    날씨 정기 업데이트
    """
    global weather_data_dict

    lock.acquire()
    print('\n\n[날씨 정기 업데이트]')
    weather_data_dict = weather_api.get_today_weather()
    lock.release()


def schedule_thread():
    schedule.every().minute.at(':50').do(weather_update)
    # schedule.every().hour.at(':50').do(weather_update)
    while True:
        schedule.run_pending()
        time.sleep(1)


def threaded(client_socket, addr):
    print(str(addr), "thread.")
    while True:
        try:
            # recvData = client_socket.recv(1024).decode('UTF-8')
            # data = str(recvData)
            data = str(client_socket.recv(1024).decode('UTF-8'))
            print('받은 데이터: ', data)
            if not data:
                print('받은 데이터가 없습니다.')
                break
            elif data == 'exit':
                break
            elif data == 'weather':
                send_weather()
            else :
                read_send(data)
        except ConnectionResetError as e:
            print('ConnectionResetError: ', e)
            client_socket.send('ConnectionResetError: threaded()'.encode('UTF-8'))
        except error as e:
            print('ERROR: ', e)
            client_socket.send('ERROR: threaded()'.encode('UTF-8'))
    client_socket.close()
    print(str(addr), '접속이 종료되었습니다.')


def run_accept_thread():
    global client_socket, addr
    server_socket.listen(1)  # 맵핑된 소켓을 연결 요청 대기 상태로 전환
    print('서버 가동 완료... ')
    while True:
        print("접속 대기중...")
        try:
            client_socket, addr = server_socket.accept()
            # thread = threading.Thread(target=threaded(client_socket, addr), daemon=True)
            # thread.start()
            # thread.join()
            threading.Thread(target=threaded(client_socket, addr), daemon=True).start()
        except error as e:
            print(e)


if __name__ == '__main__':
    IP = 'localhost'
    PORT = 9008

    lock = threading.Lock()

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((IP, PORT))
    print("서버 가동중 ...\t IP: {0}, PORT: {1}".format(IP, PORT))

    weather_data_dict = weather_api.get_today_weather()
    weather_thread = threading.Thread(target=schedule_thread, daemon=True)
    # accept_thread = threading.Thread(target=run_accept_thread)
    weather_thread.start()
    # accept_thread.start()
    # weather_thread.join()
    # accept_thread.join()

    server_socket.listen(1)  # 맵핑된 소켓을 연결 요청 대기 상태로 전환
    print('서버 가동 완료... ')
    while True:
        print("접속 대기중...")
        try:
            client_socket, addr = server_socket.accept()
            print(str(addr), "에서 접속되었습니다.")
            threading.Thread(target=threaded(client_socket, addr)).start()
        except error as e:
            print(e)

    print('server 종료')
    server_socket.close()
