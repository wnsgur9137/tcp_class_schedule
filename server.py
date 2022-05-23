import socket
import threading

HOST = 'localhost' # Server IP
PORT = 9008 # PORT
lock = threading.Lock() # syncronized 동기화를 진행하는 스레드

class UserManager:
    """
    사용자 관리 및 채팅 메세지 전송을 담당하는 클래스
    1. 채팅 서버로 입장한 사용자의 등록
    2. 채팅을 종료하는 사용자의 퇴장 관리
    3. 사용자가 입장하고 퇴장하는 관리
    4. 사용자가 입력한 메세지를 채팅 서버에 접속한 모두에게 전송
    """
    pass