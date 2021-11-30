from server_socket import ServerSocket
import json


if __name__ == "__main__":
    my_sock = ServerSocket(host='127.0.0.1', port=3131)

    @my_sock.add_event("login")
    def login(request):
        return json.dumps(my_sock.LOGIN.login(request))

    @my_sock.add_event("ping")
    def ping(request):
        return json.dumps({'error':False, 'message':'pong'})

    my_sock.start()
    my_sock.wait_for_connections()