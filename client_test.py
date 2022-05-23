import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("localhost", 9008))
sock.send('Hello'.encode())