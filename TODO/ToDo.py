from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTableView, QComboBox , QTimeEdit
from PyQt5 import QtCore , QtGui , QtWidgets , Qt
from PyQt5.uic import loadUi
import sys

class Task(QMainWindow):
    def __init__(self):
        super(Task , self).__init__()
        loadUi("todo.ui" , self)
        
        self.title = self.findChild(QComboBox , 'title')
        self.stage = self.findChild(QComboBox , 'stage')
        self.set = self.findChild(QPushButton , 'set')
        self.status = self.findChild(QTableView , 'status')
        self.start = self.findChild(QTimeEdit , 'start')
        self.end = self.findChild(QTimeEdit , 'end')
        
        self._translate = QtCore.QCoreApplication.translate
        self.counter = 1
        self.history = {}
        self.colors = {"To Do":(0,100,150),
                       "Hold":(200,50,50),
                       "In Progress":(200,150,0),
                       "Done":(10,200,100)}
        
        self.set.clicked.connect(self.add_item)
        # self.title.textActivated.connect(self.add_item)
        # self.title.textActivated['QString'].connect(self.title.clearEditText)
        self.stage.textActivated['QString'].connect(self.add_item)
        self.stage.textActivated['QString'].connect(self.title.clearEditText)
        
        
        
    def add_item(self):
        
        start_time = self.start.text()
        end_time = self.end.text()
        
        title_txt = self.title.currentText()
        stage_txt = self.stage.currentText()
        
        self.check_title(title_txt , stage_txt , start_time , end_time)
                        
        self.add_row()
        
        for element in range(self.counter-1):
            title_txt = self.history[element+1][0]
            stage_txt = self.history[element+1][1]
            start_time = self.history[element+1][2]
            end_time = self.history[element+1][3]
            
            self.add_title(title_txt , element)
            self.add_stage(stage_txt , element)
            self.add_start(start_time , element)
            self.add_end(end_time , element)
            
        # print(self.history)
    
    
    
    
    def add_title(self , title_txt , element):
        pos = QtWidgets.QTableWidgetItem()
        pos.setTextAlignment(QtCore.Qt.AlignCenter)
        
        brush = QtGui.QBrush(QtGui.QColor(150, 150, 150))
        brush.setStyle(QtCore.Qt.SolidPattern)
        pos.setForeground(brush)
        
        pos.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        
        self.status.setItem(element , 0 , pos)
        pos = self.status.item(element , 0)
        pos.setText(self._translate("window", title_txt))
    
    
    
    
    
    def add_stage(self , stage_txt  , element):
        pos = QtWidgets.QTableWidgetItem()
        pos.setTextAlignment(QtCore.Qt.AlignCenter)
        
        r,g,b = self.colors[stage_txt]
        brush = QtGui.QBrush(QtGui.QColor(r,g,b))
        brush.setStyle(QtCore.Qt.SolidPattern)
        pos.setForeground(brush)
        
        pos.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        
        self.status.setItem(element , 1 , pos)
        pos = self.status.item(element , 1)
        pos.setText(self._translate("window", stage_txt))
    
    
    
    
    
    def add_start(self , start_time  , element):
        pos = QtWidgets.QTableWidgetItem()
        pos.setTextAlignment(QtCore.Qt.AlignCenter)
        
        brush = QtGui.QBrush(QtGui.QColor(150,150,150))
        brush.setStyle(QtCore.Qt.SolidPattern)
        pos.setForeground(brush)
        
        pos.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        
        self.status.setItem(element , 2 , pos)
        pos = self.status.item(element , 2)
        pos.setText(self._translate("window", start_time))
    
    
    
    
    
    def add_end(self , end_time  , element):
        pos = QtWidgets.QTableWidgetItem()
        pos.setTextAlignment(QtCore.Qt.AlignCenter)
        
        brush = QtGui.QBrush(QtGui.QColor(150,150,150))
        brush.setStyle(QtCore.Qt.SolidPattern)
        pos.setForeground(brush)
        
        pos.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        
        self.status.setItem(element , 3 , pos)
        pos = self.status.item(element , 3)
        pos.setText(self._translate("window", end_time))
        
        
        
        
        
    def check_title(self , title_in , stage_in , start_time , end_time):

        exist = False
        
        for item in self.history:
            title_txt = self.history[item][0]
            stage_txt = self.history[item][1]
            
            if title_txt == title_in:
                exist = True
                
                if stage_txt == stage_in:
                    break
                
                else:
                    self.history[item] = (title_txt , stage_in , start_time , end_time)
                
        if exist == False:
            self.history[self.counter] = (title_in , stage_in , start_time , end_time)
            self.counter += 1
    
    
    
    
    
    def add_row(self):
        self.status.setRowCount(self.counter-1)
        
        for row in range(self.counter-1):
            item = QtWidgets.QTableWidgetItem()
            
            self.status.setVerticalHeaderItem(row, item)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            
            item = self.status.verticalHeaderItem(row)
            item.setText(self._translate("window", str(row+1)))  
    
    def fix(self):
        input = self.title.currentText()
        
        # for item in self.history:
        #     if self.history[item][0] == input:
                
        #         break       
            
    
    
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Task()
    window.show()
    sys.exit(app.exec_())