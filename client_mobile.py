import socket
import json

def main():
    host = 'localhost'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.connect((host, port))
        print("サーバーに接続しました。")
        user_name =input("ユーザー名を入力してください: ")
        room_name = input("チャットルーム名を入力してください（作成または参加）: ")
        operation = input("操作を選択してください（create/join）: ")

        message = json.dumps({'room_name': room_name, 'operation': operation,'user_name': user_name})
        tcp_socket.send(message.encode())

        response = tcp_socket.recv(1024).decode()
        print(f"サーバーからの応答: {response}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        if response:
            try:
                response_data = json.loads(response)

                if response_data['status'] == 'ok':
                    
                    
                    print("リクエストが成功しました。チャットを開始します。")
                    while True:
                        message =input("メッセージを入力してください。")
                        udp_socket.sendto(message.encode(), (host, 12346))
                        response,data =udp_socket.recvfrom(1024)
                        print(f"サーバーからの応答: {response.decode()}")
                        
                    # ここでチャット関連の処理を追加
                else:
                    print(f"エラー: {response_data['message']}")
            except json.JSONDecodeError:
                print("サーバーからの応答が不正です。")
        else:
            print("サーバーからの応答が空です。")

if __name__ == '__main__':
    main()