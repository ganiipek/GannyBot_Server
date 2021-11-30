import socket
import threading
import json
from database import database

class Login:
    def __init__(self):
        self.ONLINEDICT = []
        self.db = database()
        self.db.connect()

    def login(self, request):
        result = self.db.select("SELECT * FROM users WHERE email=%s and password=%s", (request["email"], request["password"]))
        if len(result) == 0:
            return {
                "error": True,
                "message": "Email or password is incorrect!"
            }
        elif result[0]["active"] == 0:
            return {
                "error": True,
                "message": "Your account is inactive!"
            }
        elif result[0]["active"] == 1:
            if self.checkList(result[0]["id"]):
                return{
                    "error": True,
                    "message": "This account is already online."
                }
            else:
                self.addOnlineList(result[0]["id"], request["ip"])
                return{
                    "error": False,
                    "message": "Login successful"
                }
        else:
            return {
                "error": True,
                "message": "An unknown error has occurred!"
            }

    def addOnlineList(self, account_id, client_ip):
        self.ONLINEDICT.append({account_id:client_ip})

    def removeOnlineList(self, client_ip):
        for key, value in self.ONLINEDICT.copy().items():
            if value == client_ip:
                self.ONLINEDICT.remove(key)

    def checkList(self, account_id):
        if account_id in self.ONLINEDICT:
            return True

        return False

class ServerSocket:
    def __init__(self, host='127.0.0.1', port=3131, buffersize=1024):
        self.host = host
        self.port = port
        self.buffersize = buffersize
        self.clients = []
        self.event_functions = {}
        self.LOGIN = Login()

    def start(self):
        ADDR = (self.host, self.port)
        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER.bind(ADDR)
        self.SERVER.listen()

    def close(self):
        self.SERVER.close()

    def wait_for_connections(self):
        print("Server initiated, Waiting for connections.")
        while True:
            client, client_address = self.SERVER.accept()
            self.clients.append(client)
            print("%s:%s is connected." % client_address + f" Current Client Count: {len(self.clients)}")
            x = threading.Thread(target=self.client_handler, args=[client], daemon=True)
            x.start()

    def message_to_json(self, keys, values):
        data_dict = dict(zip(keys, values))
        json_string = json.dumps(data_dict)
        return json_string.replace('\"', '"')

    def client_handler(self, client):
        while True:
            try:
                request = client.recv(1024).decode("utf8")
                print(request)
            except ConnectionResetError:
                break

            if not request:
                break

            try:
                request = json.loads(str(request).replace("'", '"'))
            except Exception as error:
                print(client.getpeername(), error)
                message = '{"error":True, "message":"Invalid JSON format"}'
                print(client.getpeername(), message)
                self.send_message(client, message.encode())

            try:
                request["ip"], request["port"] = client.getpeername()
                data = self.call_event_function(request["type"], request)
                message = data
                self.send_message(client, message.encode())

            except Exception as ex:
                message = '{"error":True, "message":"An error has occured! Check socket server program error logs."}'
                print(client.getpeername(), message)
                self.send_message(client, message.encode())
                print(ex)
                break

        self.clients.remove(client)
        print(f"Client {client.getpeername()} has disconnected. Current Client Count: {len(self.clients)}")
        client.close()

    def send_message(self, client, message):
        try:
            client.sendall(message)
        except Exception as error:
            print("messageSend_error", error)
            return False
        return True

    def call_event_function(self, request_type, *args, **kwargs):
        function_return = self.event_functions[request_type](*args, **kwargs)

        if not isinstance(function_return, str):
            raise TypeError(f"Event function {self.event_functions[request_type]} has non string return value.")
        else:
            return function_return

    def add_event(self, request_type):
        if not isinstance(request_type, str):
            raise TypeError("request_type must be string")

        def decorator(func):
            self.event_functions[request_type] = func

            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                return result

            return wrapper

        return decorator


if __name__ == "__main__":
    my_sock = ServerSocket(host='127.0.0.1', port=3131)

    @my_sock.add_event("login")
    def login(request):
        print("client: ", request)
        return json.dumps(my_sock.LOGIN.login(request))
        
    my_sock.start()
    my_sock.wait_for_connections()