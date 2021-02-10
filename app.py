from layout import MyLayout
# from typing import Collection, Sequence
# from PyQt5 import QtWidgets
from PyQt5.QtCore import  QCoreApplication
from PyQt5.QtWidgets import QAction, QFileDialog, QMainWindow, QMenu, QMessageBox

MESSAGE = None

class MyApp(QMainWindow):                       # QMainWindow 클래스 상속
    def __init__(self, parent = None):                         # 생성자
        super(MyApp, self).__init__()           # 상위 객체 생성(QMainWindow 생성자 호출)
        self.main_widget = MyLayout(self)
        self.setCentralWidget(self.main_widget)
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(600, 300, 800, 600)    # 창이 뜨는 위치와 크기 조절
        self.setWindowTitle('말뭉치 단어 찾기 프로그램')

        # self.statusBar()                        # 상태 표시줄 생성
        # self.statusBar().showMessage('hello')
        self.myStatusBar = self.statusBar()
        self.myStatusBar.showMessage('hello')

        
        self.makeMenuBar()

        self.show()

    def makeMenuBar(self):
        obj = self.menuBar()
        menuBar_file = obj.addMenu('File')     # 메뉴 바 내의 그룹 생성
        menuBar_edit = obj.addMenu('Edit')

        menuBar_file_exit = QAction('Exit', self)       # 메뉴 객체 생성
        menuBar_file_exit.setShortcut('Ctrl+Q')
        menuBar_file_exit.setStatusTip('누르면... 안녕')
        menuBar_file_exit.triggered.connect(QCoreApplication.instance().quit)

        menuBar_file_new = QMenu('New', self)

        menuBar_file_new_newFile = QAction('새로운 파일 열기', self)
        menuBar_file_new_openFile = QAction('기존 파일 열기', self)

        menuBar_file_new_openFile.triggered.connect(self.pushButton_handler)

        menuBar_file_new.addAction(menuBar_file_new_newFile) # 서브 메뉴 등록
        menuBar_file_new.addAction(menuBar_file_new_openFile)

        menuBar_file.addMenu(menuBar_file_new)
        menuBar_file.addAction(menuBar_file_exit)          # 메뉴 등록

    def pushButton_handler(self):
        print("Button pressed")
        self.open_dialog_box()

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        print(filename)
        print(path)
    
    def closeEvent(self, QCloseEvent):
        answer = QMessageBox.question(self, '종료 확인', '종료하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if answer == QMessageBox.Yes:
            QCloseEvent.accept()
        elif answer == QMessageBox.No:
            QCloseEvent.ignore()