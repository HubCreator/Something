from parsing import Parsing
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QAction, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenu, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

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

class Sub(QWidget):
    def __init__(self):
        super(Sub, self).__init__()
        self.rowSize = 2
        self.colSize = 2
        self.initLayout()

    def initLayout(self):
        self.vb = QVBoxLayout()
        self.setLayout(self.vb)

        self.hbTop = QHBoxLayout()
        self.hbMid = QVBoxLayout()
        self.hbMid_search = QHBoxLayout()
        self.hbBot = QHBoxLayout()

        self.vb.addLayout(self.hbTop)
        self.vb.addLayout(self.hbMid)
        self.vb.addStretch()
        self.vb.addLayout(self.hbBot)

        self.lbl = QLabel("검색할 어절을 입력하세요")
        self.ln = QLineEdit()           # input words
        self.btn1 = QPushButton("검색")
        self.btn2 = QPushButton("지우기")
        self.btn3 = QPushButton("출력하고 지우기")

        self.createTable()
        
        self.hbTop.addWidget(self.lbl)
        self.hbMid.addWidget(self.table)

        self.hbMid_search.addWidget(self.ln)
        self.hbMid_search.addWidget(self.btn1)

        self.hbMid.addLayout(self.hbMid_search)

        self.hbBot.addWidget(self.btn2)
        self.hbBot.addStretch()
        self.hbBot.addWidget(self.btn3)

        self.btn1.clicked.connect(self.prt_line)
        self.btn2.clicked.connect(self.del_line)
        self.btn3.clicked.connect(self.prt_del)

    def prt_line(self):
        try:
            contents = Parsing(self.ln.text())
            for r in range(self.rowSize):
                self.table.setItem(r, 0, QTableWidgetItem(contents.result[r]["form"]))
        except e:
            for r in range(self.rowSize):
                for c in range(self.colSize):
                    self.table.setItem(r, c, QTableWidgetItem(""))

    def del_line(self):
        self.ln.clear()

    def prt_del(self):
        self.prt_line()
        self.del_line()

    def createTable(self):
        self.table = QTableWidget()
        self.table.setRowCount(self.rowSize)
        self.table.setColumnCount(self.colSize)
        self.table.setHorizontalHeaderLabels(('해당 문장', '출처'))
        