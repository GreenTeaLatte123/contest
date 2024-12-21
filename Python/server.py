import socket

HOST = 'localhost'
PORT = 8080
interval = 0.5

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(0)

print(f"서버 대기 중: {HOST}:{PORT}")

client_socket, addr = server_socket.accept()
print(f"연결됨: {addr}")


client_socket.close()
server_socket.close()