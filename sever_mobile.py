import json
import socket
import threading
import uuid

class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.rooms = {}
        self.room_lock = threading.Lock()

    def making_token(self):
        return str(uuid.uuid4())

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode()
            message = json.loads(data)
            room_name = message.get('room_name')
            operation = message.get('operation')
            user_name = message.get('user_name')

            with self.room_lock:
                if operation == 'create':
                    if room_name not in self.rooms:
                        user_token = self.making_token()
                        self.rooms[room_name] = {user_token: user_name}
                        response = {'status': 'ok', 'token': user_token}
                    else:
                        response = {'status': 'error', 'message': 'Room already exists'}
                elif operation == 'join':
                    if room_name in self.rooms:
                        user_token = self.making_token()
                        self.rooms[room_name][user_token] = user_name
                        response = {'status': 'ok', 'token': user_token}
                    else:
                        response = {'status': 'error', 'message': 'Room does not exist'}

            client_socket.sendall(json.dumps(response).encode())
        finally:
            client_socket.close()

    def start(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            

if __name__ == '__main__':
    server = ChatServer()
    server.start()