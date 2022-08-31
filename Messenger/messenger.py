from PyQt5.QtWidgets import QApplication , QMainWindow ,QLineEdit , QPushButton , QTextEdit , QTableView , QComboBox
from PyQt5 import QtCore , QtGui
from PyQt5.uic import loadUi
import sys
import json
from socket import *

class Chat(QMainWindow):
    def __init__(self):
        super(Chat , self).__init__()
        loadUi("raw.ui" , self)
        
        self.key = self.findChild(QLineEdit , 'key')
        self.ip = self.findChild(QLineEdit , 'ip')
        self.port = self.findChild(QLineEdit , 'port')
        self.run = self.findChild(QPushButton , 'run')
        self.view = self.findChild(QTextEdit , 'view')
        self.line = self.findChild(QLineEdit , 'line')
        self.send = self.findChild(QPushButton , 'send')
        self.status = self.findChild(QComboBox , 'status')
        self.status_table = self.findChild(QTableView , 'status_table')
        self.note = self.findChild(QTextEdit , 'note')
        
        
        self.run.clicked.connect(self.connect_to_server)
        self.run.clicked.connect(self.current_status)
        self.send.clicked.connect(self.check_msg)
        self.line.returnPressed.connect(self.check_msg)
        self.send.clicked.connect(self.line.clear)
        self.status.currentIndexChanged.connect(self.current_status)
        
        self._translate = QtCore.QCoreApplication.translate
        self.state_pos = {'0':((0,0),(0,1)),'1':((1,0),(1,1)),'2':((2,0),(2,1)),'3':((3,0),(3,1)),'4':((4,0),(4,1))}
        self.status_list = []
        self.FORMAT = 'utf-8'
        self.client = socket(AF_INET , SOCK_STREAM)
        
        
    
    def check_msg(self):
        message = self.line.text()
        print(f"msg : {message}")
        checked = False
                
        for char in message: 
            if char == ' ':
                checked = False
                                
            else:
                checked = True
                break
                        
        if checked == True:
            self.make_msg(message)
            
    def connect_to_server(self):
        ip = str(self.ip.text())
        port = int(self.port.text())
                
        # try:
        self.client.connect((ip , port))
                        
        # except:
        #     self.show.append(f"<Attention> ~ Can't Connect to server!")
            
            
    def current_status(self):
        status = self.status.currentText()
        key = self.key.text()
                
        frame = {"KEY":key,"TXT":status,"TRACK":'True'}
                
        message = json.dumps(frame)
                
        self.send_to_server(message)
    
    
    
    def make_msg(self , message):
        key = self.key.text()
                
        frame = {"KEY":key,"TXT":message,"TRACK":'False'}
                
        message_ready = json.dumps(frame)
                
        self.send_to_server(message_ready)
    
    
        
    
    def send_to_server(self , message):
        self.client.send(message.encode(self.FORMAT))
                
        self.recv_msg()
        
        
    def recv_msg(self):
        # try:
            message_recv = self.client.recv(2048).decode(self.FORMAT)
                        
            track = str(json.loads(message_recv)["TRACK"])
                
            if track == 'True':
                message = str(json.loads(message_recv)["TXT"])
                key = str(json.loads(message_recv)["KEY"])
                                    
                self.set_status(key , message)
                                    
            else:
                message = str(json.loads(message_recv)["TXT"])
                key = str(json.loads(message_recv)["KEY"])
                                
                self.view.append(f"<{key}> ~ {message}")
                                
        # except:
        #     self.check_msg()
        
    
    
    def set_status(self , key , status):
        exist = False
                
        for name in self.status_list:
            if name[0] == key:
                exist = True
                index = self.status_list.index(name)
                break
                        
        if exist == True:
            self.status_list[index][1] = status
                
        if exist == False:
            self.status_list.append([key , status])
                        
        for i in enumerate(self.status_list):
            position = self.state_pos[str(i[0])]
                        
            item = self.status_table.item(position[0][0] , position[0][1])
            item.setText(self._translate("messenger", i[1][0]))
                        
            item = self.status_table.item(position[1][0] , position[1][1])
            item.setText(self._translate("messenger", i[1][1]))
        
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Chat()
    window.show()
    sys.exit(app.exec_())