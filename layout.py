from os import curdir, error, memfd_create, terminal_size
from sys import setrecursionlimit

from PyQt5 import QtGui
from parsing import Parsing
from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import QCheckBox, QComboBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

COL_SIZE = 5
ROW_SIZE = 10
CURRENT_CONTENTS = None
SELECTED_CATEGORIES = []
SEARCH_ALL = False

class MyLayout(QWidget):
    def __init__(self, parent):
        super(MyLayout, self).__init__(parent)
        self.parent = parent
        
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
        self.ln = QLineEdit()           # input words
        self.btn1 = QPushButton("검색")

        self.option_row = QComboBox(self)
        self.option_row.addItem("10")
        self.option_row.addItem("15")
        self.option_row.addItem("20")
        self.option_row.addItem("25")
        self.option_row.addItem("30")
        self.option_row.addItem("모두_출력")

        self.category_checkBox1 = QCheckBox("단어", self)
        self.category_checkBox2 = QCheckBox("문장", self)
        self.category_checkBox3 = QCheckBox("어절", self)
        self.category_checkBox4 = QCheckBox("출전", self)

        self.hbTop.addWidget(self.lbl)
        self.hbMid.addWidget(self.table)

        self.hbBot_option_row.addWidget(self.option_row)
        self.hbBot_option_category.addWidget(self.category_checkBox1)
        self.hbBot_option_category.addWidget(self.category_checkBox2)
        self.hbBot_option_category.addWidget(self.category_checkBox3)
        self.hbBot_option_category.addWidget(self.category_checkBox4)
        self.hbBot_input.addWidget(self.ln)
        self.hbBot_input.addWidget(self.btn1)

        self.option_row.activated[str].connect(self.onOptionRowActivated)
        self.btn1.clicked.connect(self.searchData)
        self.category_checkBox1.stateChanged.connect(self.onCheckBox1_checked)
        self.category_checkBox2.stateChanged.connect(self.onCheckBox1_checked)
        self.category_checkBox3.stateChanged.connect(self.onCheckBox1_checked)
        self.category_checkBox4.stateChanged.connect(self.onCheckBox1_checked)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
            self.searchData()
        

    def onCheckBox1_checked(self, state):
        global SELECTED_CATEGORIES
        a = self.sender()
        
        if state == Qt.Checked:
            SELECTED_CATEGORIES.append(a.text())
        else:
            print("unChecked")
            SELECTED_CATEGORIES.remove(a.text())
        

    def onOptionRowActivated(self, text):
        global ROW_SIZE
        global SEARCH_ALL

        self.parent.myStatusBar.showMessage("")

        if str(text) == "모두_출력":
            ROW_SIZE = 100  # 초기 기본값
            SEARCH_ALL = True
        else:            
            SEARCH_ALL = False
            ROW_SIZE = int(text)

        self.reAppendTable()
        

    def wipeTableData(self):
        for r in range(ROW_SIZE):       # Table 초기화
                for c in range(COL_SIZE):
                    self.table.setItem(r, c, QTableWidgetItem(""))

    def createTable(self):
        global ROW_SIZE
        global COL_SIZE
        global SEARCH_ALL
        global CURRENT_CONTENTS
        
        self.table = QTableWidget()
        
        if SEARCH_ALL == True:
            self.table.setRowCount(ROW_SIZE)
        else:
            self.table.setRowCount(ROW_SIZE)
        self.table.setColumnCount(COL_SIZE)

    def reAppendTable(self):
        self.hbMid.removeWidget(self.table)
        self.table.deleteLater()
        self.table = None
        self.createTable()
        self.hbMid.addWidget(self.table)
        self.wipeTableData()

    def changeStatusBar(self):
        global SELECTED_CATEGORIES
        global CURRENT_CONTENTS

        if "단어" in SELECTED_CATEGORIES:
            if "어절" in SELECTED_CATEGORIES:
                self.message = "해당 단어의 갯수 >> " + str(CURRENT_CONTENTS.word_result_count) + ", 해당 어절의 갯수 >> " + str(CURRENT_CONTENTS.soundBlock_result_count)
            else:
                self.message = "해당 단어의 갯수 >> " + str(CURRENT_CONTENTS.word_result_count)

        elif "어절" in SELECTED_CATEGORIES:
            if "단어" in SELECTED_CATEGORIES:
                self.message = "해당 단어의 갯수 >> " + str(CURRENT_CONTENTS.word_result_count) + ", 해당 어절의 갯수 >> " + str(CURRENT_CONTENTS.soundBlock_result_count)
            else:
                self.message = "해당 어절의 갯수 >> " + str(CURRENT_CONTENTS.soundBlock_result_count)

        else:
                self.message = "해당 어절의 갯수 >> " + str(CURRENT_CONTENTS.soundBlock_result_count)

        self.parent.myStatusBar.showMessage(self.message)

    def printData(self, keywords, r):
        global CURRENT_CONTENTS

        dic_t = {"문장" : "form", "출전" : "metadata", "어절" : "form", "단어" : "form"}

        if keywords == "문장":
            key = dic_t[keywords]
            if CURRENT_CONTENTS.sentence_result[r] == None:
                self.table.setItem(r, 0, QTableWidgetItem(""))
            self.table.setItem(r, 0, QTableWidgetItem(CURRENT_CONTENTS.sentence_result[r][key]))
        if keywords == "단어":
            key = dic_t[keywords]
            # if CURRENT_CONTENTS.word_result[r] == None:
            #     self.table.setItem(r, 1, QTableWidgetItem(""))
            if CURRENT_CONTENTS.word_result_with_soundBlock[r] == "":
                self.table.setItem(r, 1, QTableWidgetItem(""))
            else:
                self.table.setItem(r, 1, QTableWidgetItem(CURRENT_CONTENTS.word_result_with_soundBlock[r][key] ))
        if keywords == "어절":
            key = dic_t[keywords]
            if CURRENT_CONTENTS.soundBlock_result[r] == None:
                self.table.setItem(r, 2, QTableWidgetItem(""))
            self.table.setItem(r, 2, QTableWidgetItem(CURRENT_CONTENTS.soundBlock_result[r][key] ))
        if keywords == "출전":
            key = dic_t[keywords]
            if CURRENT_CONTENTS.origin_result[r][key]["title"] == "":
                self.table.setItem(r, 3, QTableWidgetItem(CURRENT_CONTENTS.origin_result[r][key]["publisher"]))
            else:
                self.table.setItem(r, 3, QTableWidgetItem(CURRENT_CONTENTS.origin_result[r][key]["title"]))

    def searchData(self):
        global ROW_SIZE
        global COL_SIZE
        global CURRENT_CONTENTS # Parsed data
        global SELECTED_CATEGORIES
        global SEARCH_ALL

        CURRENT_CONTENTS = Parsing(self.parent.myObjectFile, self.ln.text())

        # self.reAppendTable()
        self.wipeTableData()

        try:
            if SEARCH_ALL == True:
                self.changeStatusBar()

                # ROW_SIZE = CURRENT_CONTENTS.result_count
                if ("단어" and "어절") in SELECTED_CATEGORIES:
                    ROW_SIZE = CURRENT_CONTENTS.soundBlock_result_count
                if "단어" in SELECTED_CATEGORIES:
                    ROW_SIZE = CURRENT_CONTENTS.word_result_count
                if "어절" in SELECTED_CATEGORIES:
                    ROW_SIZE = CURRENT_CONTENTS.soundBlock_result_count

                self.reAppendTable()
                for keywords in SELECTED_CATEGORIES:    # 어쨌든 for문이 2번 돌아가는 거 아닌가..?
                    if ROW_SIZE:
                        for r in range(ROW_SIZE):   # ROW_SIZE 만큼만 출력
                            self.printData(keywords, r)

            self.changeStatusBar()
            for keywords in SELECTED_CATEGORIES:    # 어쨌든 for문이 2번 돌아가는 거 아닌가..?
                # if("단어" and "어절") in SELECTED_CATEGORIES:
                #     ROW_SIZE = CURRENT_CONTENTS.soundBlock_result_count
                # if "단어" in SELECTED_CATEGORIES:
                #     ROW_SIZE = CURRENT_CONTENTS.word_result_count
                # if "어절" in SELECTED_CATEGORIES:
                #     ROW_SIZE = CURRENT_CONTENTS.soundBlock_result_count
                    
                if (ROW_SIZE >= CURRENT_CONTENTS.soundBlock_result_count) and (SEARCH_ALL == False):    # 결과의 갯수와 ROW_SIZE 비교
                    for r in range(CURRENT_CONTENTS.soundBlock_result_count):   # ROW_SIZE 만큼만 출력
                        self.printData(keywords, r)


                if (ROW_SIZE < CURRENT_CONTENTS.soundBlock_result_count) and (SEARCH_ALL == False):
                    for r in range(ROW_SIZE):   # ROW_SIZE 만큼만 출력
                        self.printData(keywords, r)


                    
        except error:
            self.wipeTableData()


