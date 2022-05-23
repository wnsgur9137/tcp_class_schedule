server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9008))
server_socket.listen(0) # 클라이언트의 연결요청을 기다리는 상태

client_socket, addr = server_socket.accept() # 연결 요청 수락 -> IP/PORT return

data = client_socket.recv(65535) # 클라이언트로부터 데이터를 받는다. (출력되는 버퍼 사이즈)

print("받은 데이터:", data.decode()) # 받은 데이터 해석