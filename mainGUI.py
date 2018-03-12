from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import sys
import socket
from numpy import long
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
import os

fileName = ""
cancel=False
class UIClient(QDialog):
    status = "Not Connected"
    BUFFER_SIZE = 1024
    BUFFER_SIZE_10 = 1126
    BUFFER_SIZE_500 = 5120
    s = socket.socket()
    text = ""


    def __init__(self):
        super(UIClient, self).__init__()
        loadUi('GUIClient.ui', self)
        self.setWindowTitle("GUIClient")
        self.connect()
        self.setup()
        self.show()


    def setup(self):
        self.pushButton_2.clicked.connect(self.openFile)
        global fileName
        print(fileName)
        self.pushButton_3.clicked.connect(self.cancel)
        self.pushButton.clicked.connect(self.download)



    def connect(self):
        host = '0.0.0.0'
        print(host)
        port = 5009
        self.s.connect((host, port))
        self.status = (self.s.recv(self.BUFFER_SIZE_500)).decode("utf-8")
        self.label_2.setText(self.status)

    def cancel(self):
        self.s.send(b"cancel")


    def download(self):

        #filename = input("Filename? -> ")
        global fileName
        filename = fileName
        print(filename)
        if filename != 'q':
            self.s.send(bytes(filename, encoding="ascii"))
            data = self.s.recv(self.BUFFER_SIZE_500)
            if data[:6] == b'EXISTS':
                filesize = long(data[7:])
                print("File size: " + str(filesize))
                self.label_3.setText(("File exists, " + str(filesize) + "Bytes, start download-> "))
                self.s.send(b"OK")
                f = open('./DataRecibida/new_' + filename, 'wb')
                data = self.s.recv(self.BUFFER_SIZE_500)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = self.s.recv(self.BUFFER_SIZE_500)
                    totalRecv += len(data)
                    f.write(data)
                    percentage = "{0:.2f}".format((totalRecv / float(filesize)) * 100)
                    self.progressBar.setValue(int(float(percentage)))
                    print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done")
                    print("Package: "+ str(totalRecv) +" bytes")
                self.label_3.setText("Download Complete!")
                f.close()
            else:
                print("File Does Not Exist!")

        #self.s.close()

    def openFile(self):
        filesame,_ = QFileDialog.getOpenFileName(self, 'Open File','./Server')
        global fileName
        fileName = os.path.basename(filesame)
        self.label_4.setText(os.path.basename(fileName))






if __name__ == '__main__':

    def run():
        app = QApplication(sys.argv)
        widget = UIClient()
        sys.exit(app.exec_())

run()
