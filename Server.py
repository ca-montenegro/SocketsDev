import socket
import threading
import os

BUFFER_SIZE_original = 1024
BUFFER_SIZE_10 = 1126
BUFFER_SIZE_500 = 5120

def RetrFile(name, sock):
    sock.send(b"Connected to server")
    filename = sock.recv(BUFFER_SIZE_500)
    if os.path.isfile(filename):
        strSend = "EXISTS " + str(os.path.getsize(filename))
        sock.send(bytes(strSend,encoding="ascii"))
        userResponse = sock.recv(BUFFER_SIZE_500)
        if userResponse[:2] == b'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(BUFFER_SIZE_500)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(BUFFER_SIZE_500)
                    sock.send(bytesToSend)
    else:
        sock.send(b"ERR ")

    sock.close()


def Main():
    host = '0.0.0.0'
    port = 5009

    s = socket.socket()
    s.bind((host, port))

    s.listen(5)

    print("Server Started.")
    while True:
        c, addr = s.accept()
        print( "client connedted ip:<" + str(addr) + ">")
        t = threading.Thread(target=RetrFile, args=("RetrThread", c))
        t.start()

    s.close()


if __name__ == '__main__':
    Main()