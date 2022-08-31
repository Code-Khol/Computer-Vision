from socket import *
import threading

class Server(object):
    def __init__(self , ip , port):
        self.clients = []
        self.FORMAT = 'utf-8'
        self.server = socket(AF_INET , SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET , SO_REUSEADDR , 1)
        self.server.bind((ip , port))
        self.server.listen()
        
        def remove(client):
            if client in self.clients:
                self.clients.remove(client)
        
        
        def send_message(message , addr):
            print(message)
            for client in self.clients:
                try:
                    print("send back")
                    client.send(message.encode(self.FORMAT))
                except:
                    remove(client)
                    print("-----")
        
        
        
        def recv_message(connection):
            message = connection.recv(2048).decode(self.FORMAT)
            if message:
                print("msg recived!")
                return message
        
        
        def status(connection , addr):
            print("waiting for msg")
            while True:
                if message := recv_message(connection):
                    send_message(message , addr)
                else:
                    remove(connection)
        
        
        while True:
            print("listening ...")
            connection , addr = self.server.accept()
            self.clients.append(connection)
            threading.Thread(target=status , args=(connection , addr)).start()
        
        
        
if __name__ == "__main__":
    Server('127.0.0.1' , 8080)