from typing import Collection
from PyQt5 import QtWidgets
from PyQt5.QtGui import QCloseEvent
from parsing import Parsing
from PyQt5.QtCore import  QCoreApplication
from PyQt5.QtWidgets import QAction, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QHBoxLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QMenu, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

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
ROW_SIZE = 10
CURRENT_CONTENTS = None
SELECTED_CATEGORIES = []

class OptionWindow(QWidget):
    def __init__(self):
        super(OptionWindow,self).__init__()
        self.title = '검색 설정'
        self.left = 20
        self.top = 20
        self.height = 600
        self.width = 800
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

class Sub(QWidget):
    def __init__(self):
        super(Sub, self).__init__()
        
        self.initLayout()

    def initLayout(self):
        self.vb = QVBoxLayout()
        self.setLayout(self.vb)

        self.hbTop = QHBoxLayout()
        self.hbMid = QHBoxLayout()
        self.hbBot = QVBoxLayout()
        self.hbBot_option = QHBoxLayout()
        self.hbBot_option_row = QHBoxLayout()
        self.hbBot_option_category = QHBoxLayout()
        self.hbBot_input = QHBoxLayout()

        self.vb.addLayout(self.hbTop)
        self.vb.addLayout(self.hbMid)
        self.hbBot.addLayout(self.hbBot_option)
        self.hbBot_option.addLayout(self.hbBot_option_row)
        self.hbBot_option.addStretch()
        self.hbBot_option.addLayout(self.hbBot_option_category)
        self.hbBot.addLayout(self.hbBot_input)
        self.vb.addLayout(self.hbBot)

        self.lbl = QLabel("검색할 어절을 입력하세요")
        self.createTable()
        # self.option = QLabel("10", self)
        self.ln = QLineEdit()           # input words
        self.btn1 = QPushButton("검색")

        self.option_row = QComboBox(self)
        self.option_row.addItem("10")
        self.option_row.addItem("15")
        self.option_row.addItem("20")
        self.option_row.addItem("25")
        self.option_row.addItem("30")

        self.category_checkBox1 = QCheckBox("단어", self)
        self.category_checkBox2 = QCheckBox("문장", self)
        self.category_checkBox3 = QCheckBox("어절", self)
        self.category_checkBox4 = QCheckBox("출전", self)

        # category_checkBox1.setObjectName("단어")

        self.hbTop.addWidget(self.lbl)
        self.hbMid.addWidget(self.table)

        self.hbBot_option_row.addWidget(self.option_row)
        self.hbBot_option_category.addWidget(self.category_checkBox1)
        self.hbBot_option_category.addWidget(self.category_checkBox2)
        self.hbBot_option_category.addWidget(self.category_checkBox3)
        self.hbBot_option_category.addWidget(self.category_checkBox4)
        self.hbBot_input.addWidget(self.ln)
        self.hbBot_input.addWidget(self.btn1)

        # self.hbMid.addLayout(self.hbMid_search)

        self.option_row.activated[str].connect(self.onOptionRowActivated)
        self.btn1.clicked.connect(self.searchData)

    def onOptionRowActivated(self, text):
        global ROW_SIZE

        self.hbMid.removeWidget(self.table)
        self.table.deleteLater()
        self.table = None

        ROW_SIZE = int(text)
        self.createTable()
        self.hbMid.addWidget(self.table)


    def searchData(self):
        global ROW_SIZE
        global COL_SIZE
        global CURRENT_CONTENTS # Parsed data
        global SELECTED_CATEGORIES

        try:
            CURRENT_CONTENTS = Parsing(self.ln.text())
            # todo : 카테고리 확인 절차

            for r in range(ROW_SIZE):
                tmp = str(SELECTED_CATEGORIES[r])
                if tmp == " ":
                    self.table.setItem(r + 1, 0, QTableWidgetItem(""))
                elif tmp == "해당 단어":
                    self.table.setItem(r+1, 0, QTableWidgetItem(CURRENT_CONTENTS.word_result[r]["form"]))
                elif tmp == "해당 문장":
                    self.table.setItem(r+1, 0, QTableWidgetItem(CURRENT_CONTENTS.word_result[r]["form"])) # should change
                elif tmp == "어절 검색":
                    self.table.setItem(r+1, 0, QTableWidgetItem(CURRENT_CONTENTS.word_result[r]["form"])) # should change
                elif tmp == "출전":
                    self.table.setItem(r+1, 0, QTableWidgetItem(CURRENT_CONTENTS.word_result[r]["form"])) # should change

        except e:
            for r in range(ROW_SIZE):
                for c in range(COL_SIZE):
                    self.table.setItem(r, c, QTableWidgetItem(""))

    def createTable(self):
        global ROW_SIZE
        global COL_SIZE
        global SELECTED_CATEGORIES
        self.table = QTableWidget()

        self.table.setRowCount(ROW_SIZE)
        self.table.setColumnCount(COL_SIZE)

        category = [" ", "해당 단어", "해당 문장", "어절 검색", "출전"]
        
        # 카테고리를 콤보박스에 달기
        for j in range(0, COL_SIZE, 1):
            # self.table.setItem(0, i, QTableWidgetItem(str(j)))
            self.category_comboBox = QComboBox(self)
            for i in range(0, len(category), 1):
                self.category_comboBox.addItem(category[i])
            self.table.setCellWidget(0, j, self.category_comboBox)
            self.category_comboBox.activated[str].connect(self.onCategoryComboBoxActivated) # 카테고리의 항목이 선택됐을 때
        
        # for j in range(0, COL_SIZE, 1):
            # print(self.table.itemAt(0, j))
            # SELECTED_CATEGORIES.append(self.table.itemAt(0, j))
    
    def onCategoryComboBoxActivated(self, text):
        global SELECTED_CATEGORIES
        global CURRENT_CONTENTS
        value = str(text)
        a = self.sender()   # 누가 눌렀냐 category_comboBox
        # print(a.currentText())

        SELECTED_CATEGORIES.append(a.currentText()) # 순서 상관 X
