import socket

from numpy import long


def Main():
    host = '0.0.0.0'
    port = 5001

    s = socket.socket()
    s.connect((host, port))
    print(s.recv(1024))
    filename = input("Filename? -> ")
    if filename != 'q':
        s.send(bytes(filename,encoding="ascii"))
        data = s.recv(1024)
        if data[:6] == b'EXISTS':
            filesize = long(data[7:])
            message = input("File exists, " + str(filesize) + "Bytes, download? (Y/N)? -> ")
            if message == 'Y':
                s.send(b"OK")
                f = open('new_' + filename, 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done")
                print("Download Complete!")
                f.close()
        else:
            print("File Does Not Exist!")

    s.close()


if __name__ == '__main__':
    Main()

