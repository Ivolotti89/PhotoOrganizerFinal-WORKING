import webbrowser
from myframe import MyFrame
import script
import sys
import Logo
from PyQt5.QtCore import Qt
import time
import os
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog,QMessageBox,QApplication
from numpy import empty
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess


app=QApplication(sys.argv)
if getattr(sys,'frozen',False):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_path)
 
event_dir=[]
dName=""
emptyStr = ""
new_path = ""

form,call=uic.loadUiType("AppUI.ui")
form3,call3=uic.loadUiType("splash.ui")
form1,call1=uic.loadUiType("processing.ui")
form2,call2=uic.loadUiType("processed.ui")

class SplashScreen(call3,form3):
    def __init__(self):

        super(call3,self).__init__()
        self.setWindowTitle("Dino Foto")
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.setFixedWidth(850)
        self.setFixedHeight(580)
        self.setupUi(self)



class myApp(call,form):
    def __init__(self):
        super(call,self).__init__()
        self.setupUi(self)
        # print(width)
        self.widget.sendDirec.connect(self.setDirec)
        self.browseButton.clicked.connect(self.askD)
        self.proceedButton.clicked.connect(self.onClick)
        

    def change(self):
        self.main = ProcessingPage()
        self.main.show()
        self.close()

      
    #Getting directory from button click.
    def askD(self):
        global dName
        dName = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        self.direcText.setText(dName)
        # print("directory: ",dName)

    #Getting directory from drop event of myframe.
    def setDirec(self,directory):
        # print ("Directory",directory)
        global dName
        dName = directory
        self.direcText.setText(dName)


    #Changing UI to Processing
    def onClick(self):
        if (dName != emptyStr):
            self.change()
        else:
            eMsg = QMessageBox()
            eMsg.setIcon(QMessageBox.Critical)
            eMsg.setWindowTitle('Error')
            eMsg.setText("No Folder Selected!")
            eMsg.exec()



class ProcessingPage(call1,form1):
    def __init__(self):
        super(call1, self).__init__()
        self.setupUi(self)
        #Making a thread for executing script
        self.organize = External()
        self.runScript()
        
    
    def runScript(self):
        self.organize.countChanged.connect(self.onCountChanged)
        self.organize.finished.connect(self.onFinished)
        self.organize.start()
    
    #Getting values from script for progress bar
    def onCountChanged(self, value):
        self.pBar.setValue(value[0])
        self.iLabel.setText(value[1])
    
    
    def onFinished(self):
        self.main = ProcessedPage(self.organize.event_dir,self.organize.event_dir_lis)
        self.main.setWindowTitle("Dino Foto")
        self.setWindowIcon(QIcon('resources/dino-new.png')) 
        self.main.show()
        self.close()

class ProcessedPage(call2,form2):
    def __init__(self,event_dir,event_lis):
        super(call2, self).__init__()
        self.event_dir=event_dir
        self.event_lis1 = event_lis
        # print(self.event_lis1)
        # for items in self.event_lis1:
        #     os.mkdir(os.path.join(items+'/','final sets'))
        #     os.mkdir(os.path.join(items+'/final sets','preview'))
        # print("EVENT DIRECTORY: "+self.event_dir)
        self.setupUi(self)
        self.nextButton.clicked.connect(self.change)
        self.dashboardButton.clicked.connect(self.toDashboard)
        self.eLabel.setText(self.event_dir)
        self.viewButton.clicked.connect(self.openDirec)

    def change(self):
        self.main = myApp()
        self.main.setWindowTitle("Dino Foto")
        self.setWindowIcon(QIcon('resources/dino-new.png')) 
        self.main.show()
        self.close()

    def toDashboard(self):
        webbrowser.get("safari").open_new('www.foto-dino.de')
    
    def openDirec(self):
        subprocess.call(["open", new_path])
        


class External(QThread):
    countChanged = pyqtSignal(list)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.event_dir = None
        self.event_dir_lis = None
    
    def run(self):
        self.event_dir_lis, self.event_dir, new_path = script.mainFunc(self,dName)




if __name__ == '__main__':
    splash = SplashScreen()
    splash.show()
    time.sleep(2)
    splash.close()
    ex = myApp()
    ex.setWindowTitle("Dino Foto")
    ex.setWindowIcon(QIcon('resources/dino-new.png')) 
    ex.show()
    sys.exit(app.exec_())