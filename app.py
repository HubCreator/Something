from typing import Collection
from PyQt5 import QtWidgets
from parsing import Parsing
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QAction, QComboBox, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenu, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

# ROW_SIZE = 2
# COL_SIZE = 5

class MyApp(QMainWindow):                        # QMainWindow 클래스 상속
    def __init__(self):                         # 생성자
        super(MyApp, self).__init__()                      # 상위 객체 생성(QMainWindow 생성자 호출)
        self.setCentralWidget(Sub())
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(600, 300, 800, 600)    # 창이 뜨는 위치와 크기 조절
        self.setWindowTitle('말뭉치 단어 찾기 프로그램')

        self.statusBar()                        # 상태 표시줄 생성
        self.statusBar().showMessage('hello')
        
        # btn = QPushButton('hi', self)
        # btn.resize(btn.sizeHint())
        # btn.setToolTip('tooltip')
        # btn.move(70, 30)
        # btn.clicked.connect(QCoreApplication.instance().quit) # QCoreApplication은 모든 이벤트에 대한 처리를 한다.

        self.makeMenuBar()
        #self.initLayout()

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

        menuBar_file_new.addAction(menuBar_file_new_newFile) # 서브 메뉴 등록
        menuBar_file_new.addAction(menuBar_file_new_openFile)

        menuBar_file.addMenu(menuBar_file_new)
        menuBar_file.addAction(menuBar_file_exit)          # 메뉴 등록
    
    def closeEvent(self, QCloseEvent):
        answer = QMessageBox.question(self, '종료 확인', '종료하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if answer == QMessageBox.Yes:
            QCloseEvent.accept()
        elif answer == QMessageBox.No:
            QCloseEvent.ignore()

COL_SIZE = 5
ROW_SIZE = 3

class Sub(QWidget):
    def __init__(self):
        super(Sub, self).__init__()
        # self.colSize = COL_SIZE    # 행
        # self.rowSize = ROW_SIZE    # 열 
        self.initLayout()

    def initLayout(self):
        self.vb = QVBoxLayout()
        self.setLayout(self.vb)

        self.hbTop = QHBoxLayout()
        self.hbMid = QHBoxLayout()
        self.hbBot = QVBoxLayout()
        self.hbBot_option = QHBoxLayout()
        self.hbBot_input = QHBoxLayout()

        self.vb.addLayout(self.hbTop)
        self.vb.addLayout(self.hbMid)
        self.vb.addStretch()
        self.hbBot.addLayout(self.hbBot_option)
        self.hbBot.addLayout(self.hbBot_input)
        self.vb.addLayout(self.hbBot)

        self.lbl = QLabel("검색할 어절을 입력하세요")
        self.createTable()
        # self.option = QLabel("10", self)
        self.ln = QLineEdit()           # input words
        self.btn1 = QPushButton("검색")

        combo = QComboBox(self)
        combo.addItem("10")
        combo.addItem("15")
        combo.addItem("20")
        combo.addItem("25")
        combo.addItem("30")
        
        self.hbTop.addWidget(self.lbl)
        self.hbMid.addWidget(self.table)

        self.hbBot_option.addWidget(combo)
        self.hbBot_input.addWidget(self.ln)
        self.hbBot_input.addWidget(self.btn1)

        # self.hbMid.addLayout(self.hbMid_search)

        combo.activated[str].connect(self.onActivated)
        self.btn1.clicked.connect(self.prt_line)

    def onActivated(self, text):
        self.hbMid.removeWidget(self.table)
        self.table.deleteLater()
        self.table = None

        global ROW_SIZE
        ROW_SIZE = int(text)
        self.createTable()
        self.hbMid.addWidget(self.table)


    # def clearLayout(self, layout):
    #     while layout.count():
    #         child = layout.takeAt(0)
    #         if child.widget():
    #             child.widget().deleteLater()

    def prt_line(self):
        global ROW_SIZE
        global COL_SIZE
        try:
            contents = Parsing(self.ln.text())
            for r in range(ROW_SIZE):
                self.table.setItem(r+1, 1, QTableWidgetItem(contents.result[r]["form"]))
        except e:
            for r in range(COL_SIZE):
                for c in range(self.colSize):
                    self.table.setItem(r, c, QTableWidgetItem(""))

    def createTable(self):
        global ROW_SIZE
        global COL_SIZE
        self.table = QTableWidget()

        self.table.setRowCount(ROW_SIZE)
        self.table.setColumnCount(COL_SIZE)

        category = [" ", "해당 문장", "출처"]
        
        for j in range(0, COL_SIZE, 1):
            # self.table.setItem(0, i, QTableWidgetItem(str(j)))
            category_comboBox = QComboBox(self)
            for i in range(0, len(category), 1):
                category_comboBox.addItem(category[i])
            self.table.setCellWidget(0, j, category_comboBox)
