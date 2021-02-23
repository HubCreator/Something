from operator import eq
from changeSequence import changeSequence
from os import curdir, error, memfd_create, stat, terminal_size
from sys import setrecursionlimit

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from parsing import Parsing
from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import QCheckBox, QComboBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

COL_SIZE = 5
ROW_SIZE = 11
CURRENT_CONTENTS = None
SELECTED_CATEGORIES = ["문장", "단어", "어절", "출전"]
SEARCH_ALL = False

COL_SERIAL_NUMBER = 0
COL_SENTENCE = 1
COL_WORD = 2
COL_WORDBLOCK = 3
COL_ORIGIN = 4

STATUS_OF_SERIAL_BUTTON = "고유번호 🔼️"
STATUS_OF_SENTENCE_BUTTON = "문장 🔼️"
STATUS_OF_WORD_BUTTON = "단어 🔼️"
STATUS_OF_WORDBLOCK_BUTTON = "어절 🔼️"
STATUS_OF_ORIGIN_BUTTON = "출전 🔼️"

class MyLayout(QWidget):
    def __init__(self, parent):
        super(MyLayout, self).__init__(parent)
        self.parent = parent
        # self.list_for_sequence = []
        
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

        self.category_checkBox1 = QCheckBox("문장", self)
        self.category_checkBox1.setChecked(True)

        self.category_checkBox2 = QCheckBox("단어", self)
        self.category_checkBox2.setChecked(True)

        self.category_checkBox3 = QCheckBox("어절", self)
        self.category_checkBox3.setChecked(True)
        
        self.category_checkBox4 = QCheckBox("출전", self)
        self.category_checkBox4.setChecked(True)

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
            ROW_SIZE = 100 + 1  # 초기 기본값
            SEARCH_ALL = True
        else:            
            SEARCH_ALL = False
            ROW_SIZE = int(text) + 1

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

        global COL_SERIAL_NUMBER
        global COL_SENTENCE
        global COL_WORD
        global COL_WORDBLOCK
        global COL_ORIGIN

        global STATUS_OF_SERIAL_BUTTON
        global STATUS_OF_SENTENCE_BUTTON
        global STATUS_OF_WORD_BUTTON
        global STATUS_OF_WORDBLOCK_BUTTON
        global STATUS_OF_ORIGIN_BUTTON
        
        self.table = QTableWidget()
        self.serialButton = QPushButton(STATUS_OF_SERIAL_BUTTON)
        self.sentenceButton = QPushButton(STATUS_OF_SENTENCE_BUTTON)
        self.wordButton = QPushButton(STATUS_OF_WORD_BUTTON)
        self.wordBlockButton = QPushButton(STATUS_OF_WORDBLOCK_BUTTON)
        self.originButton = QPushButton(STATUS_OF_ORIGIN_BUTTON)

        self.table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        
        
        self.table.setRowCount(ROW_SIZE)
        self.table.setColumnCount(COL_SIZE)

        self.table.setHorizontalHeaderLabels(('1', '2', '3', '4', '5'))

        for i in range(0, ROW_SIZE, 1):
            self.table.setVerticalHeaderItem(i, QTableWidgetItem(str(i)))

        self.table.setCellWidget(0, COL_SERIAL_NUMBER, self.serialButton)
        self.table.setCellWidget(0, COL_SENTENCE, self.sentenceButton)
        self.table.setCellWidget(0, COL_WORD, self.wordButton)
        self.table.setCellWidget(0, COL_WORDBLOCK, self.wordBlockButton)
        self.table.setCellWidget(0, COL_ORIGIN, self.originButton)

        self.serialButton.clicked.connect(self.handleSequence)
        self.sentenceButton.clicked.connect(self.handleSequence)
        self.wordButton.clicked.connect(self.handleSequence)
        self.wordBlockButton.clicked.connect(self.handleSequence)
        self.originButton.clicked.connect(self.handleSequence)

    def handleSequence(self):
        global CURRENT_CONTENTS
        global ROW_SIZE
        global COL_SIZE
        global COL_SERIAL_NUMBER

        global STATUS_OF_SERIAL_BUTTON
        global STATUS_OF_SENTENCE_BUTTON
        global STATUS_OF_WORD_BUTTON
        global STATUS_OF_WORDBLOCK_BUTTON
        global STATUS_OF_ORIGIN_BUTTON

        a = self.sender()
        # print(a.text())

        if self.tmp:
            self.tmp.clear()
            
        self.tmp = [""] # tmp is for result of changed data

        self.wipeTableData()
        self.selectedCategory = None
        if a.text() == "고유번호 🔼️":
            # True is up / False is down
            self.selectedCategory = changeSequence(self.list_for_sequence, COL_SERIAL_NUMBER, True)

            STATUS_OF_SERIAL_BUTTON = "고유번호 🔽️"
            self.reAppendTable()

            for i in range(0, len(self.list_for_sequence), 1):
                for j in range(0, len(self.selectedCategory.sequence_result), 1):
                    if self.selectedCategory.sequence_result[i] == self.list_for_sequence[j][COL_SERIAL_NUMBER]:
                        self.tmp.append(self.list_for_sequence[j])

            for r in range(1, ROW_SIZE, 1):
                for c in range(0, COL_SIZE, 1):
                    if c == 0:
                        self.table.setItem(r, COL_SERIAL_NUMBER, QTableWidgetItem(str("{0}".format(int(self.tmp[r][COL_SERIAL_NUMBER])))))
                    else:
                        self.table.setItem(r, c, QTableWidgetItem(self.tmp[r][c]))

        elif a.text() == "고유번호 🔽️":
            self.selectedCategory = changeSequence(self.list_for_sequence, COL_SERIAL_NUMBER, False)

            STATUS_OF_SERIAL_BUTTON = "고유번호 🔼️"
            self.reAppendTable()

            for i in range(0, len(self.list_for_sequence), 1):
                for j in range(0, len(self.selectedCategory.sequence_result), 1):
                    if self.selectedCategory.sequence_result[i] == self.list_for_sequence[j][COL_SERIAL_NUMBER]:
                        self.tmp.append(self.list_for_sequence[j])

            for r in range(1, ROW_SIZE, 1):
                for c in range(0, COL_SIZE, 1):
                    if c == 0:
                        self.table.setItem(r, COL_SERIAL_NUMBER, QTableWidgetItem(str("{0}".format(int(self.tmp[r][COL_SERIAL_NUMBER])))))
                    else:
                        self.table.setItem(r, c, QTableWidgetItem(self.tmp[r][c]))

        elif a.text() == "문장 🔼️":
            self.selectedCategory = changeSequence(self.list_for_sequence, COL_SENTENCE, True)

            STATUS_OF_SENTENCE_BUTTON = "문장 🔽️"
            self.reAppendTable()

            for i in range(0, len(self.list_for_sequence), 1):
                for j in range(0, len(self.selectedCategory.sequence_result), 1):
                    if eq(self.selectedCategory.sequence_result[i], self.list_for_sequence[j][COL_SENTENCE]):
                        self.tmp.append(self.list_for_sequence[j])

            for r in range(1, ROW_SIZE, 1):
                for c in range(0, COL_SIZE, 1):
                    if c == 0:
                        self.table.setItem(r, COL_SERIAL_NUMBER, QTableWidgetItem(str("{0}".format(int(self.tmp[r][COL_SERIAL_NUMBER])))))
                    else:
                        self.table.setItem(r, c, QTableWidgetItem(self.tmp[r][c]))

        elif a.text() == "문장 🔽️":
            self.selectedCategory = changeSequence(self.list_for_sequence, COL_SENTENCE, False)

            STATUS_OF_SENTENCE_BUTTON = "문장 🔼️"
            self.reAppendTable()

            for i in range(0, len(self.list_for_sequence), 1):
                for j in range(0, len(self.selectedCategory.sequence_result), 1):
                    if eq(self.selectedCategory.sequence_result[i], self.list_for_sequence[j][COL_SENTENCE]):
                        self.tmp.append(self.list_for_sequence[j])
            
            for r in range(1, ROW_SIZE, 1):
                for c in range(0, COL_SIZE, 1):
                    if c == 0:
                        self.table.setItem(r, COL_SERIAL_NUMBER, QTableWidgetItem(str("{0}".format(int(self.tmp[r][COL_SERIAL_NUMBER])))))
                    else:
                        self.table.setItem(r, c, QTableWidgetItem(self.tmp[r][c]))
        else:
            pass
            
                
    def reAppendTable(self):
        self.hbMid.removeWidget(self.table)
        self.table.deleteLater()
        self.table = None
        self.createTable()
        self.hbMid.addWidget(self.table)
        self.tmp = []
        self.tmp.clear()
        self.tmp.append("")
        self.wipeTableData()

    def changeStatusBar(self):
        global SELECTED_CATEGORIES
        global CURRENT_CONTENTS

        if CURRENT_CONTENTS.fileType == True:
            if "단어" in SELECTED_CATEGORIES:
                if "어절" in SELECTED_CATEGORIES:
                    self.message = "해당 단어의 갯수 >> " + str(CURRENT_CONTENTS.sentenceType_word_result_count) + " / 해당 단어를 포함한 결과 >> " + str(CURRENT_CONTENTS.sentenceType_soundBlock_result_count)
                else:
                    self.message = "해당 단어의 갯수 >> " + str(CURRENT_CONTENTS.sentenceType_word_result_count)

            elif "어절" in SELECTED_CATEGORIES:
                if "단어" in SELECTED_CATEGORIES:
                    self.message = "해당 단어의 갯수 >> " + str(CURRENT_CONTENTS.sentenceType_word_result_count) + " / 해당 단어를 포함한 결과 >> " + str(CURRENT_CONTENTS.sentenceType_soundBlock_result_count)
                else:
                    self.message = "해당 단어를 포함한 결과 >> " + str(CURRENT_CONTENTS.sentenceType_soundBlock_result_count)

            else:
                    self.message = "해당 단어를 포함한 결과 >> " + str(CURRENT_CONTENTS.sentenceType_word_result_count)

        else:
            if "단어" in SELECTED_CATEGORIES:
                if "어절" in SELECTED_CATEGORIES:
                    self.message = "해당 단어의 갯수 >> " + str(CURRENT_CONTENTS.paragraphType_word_result_count) + " / 해당 단어를 포함한 결과 >> " + str(CURRENT_CONTENTS.paragraphType_soundBlock_result_count)
                else:
                    self.message = "해당 단어의 갯수 >> " + str(CURRENT_CONTENTS.paragraphType_word_result_count)

            elif "어절" in SELECTED_CATEGORIES:
                if "단어" in SELECTED_CATEGORIES:
                    self.message = "해당 단어의 갯수 >> " + str(CURRENT_CONTENTS.paragraphType_word_result_count) + " / 해당 단어를 포함한 결과 >> " + str(CURRENT_CONTENTS.paragraphType_soundBlock_result_count)
                else:
                    self.message = "해당 단어를 포함한 결과 >> " + str(CURRENT_CONTENTS.paragraphType_soundBlock_result_count)

            else:
                    self.message = "해당 단어를 포함한 결과 >> " + str(CURRENT_CONTENTS.paragraphType_word_result_count)

        self.parent.myStatusBar.showMessage(self.message)


    def printSearchResultData(self, r, type):
        global CURRENT_CONTENTS
        global SELECTED_CATEGORIES
        global COL_SERIAL_NUMBER
        global COL_SENTENCE
        global COL_WORD
        global COL_WORDBLOCK
        global COL_ORIGIN

        dic_t = {"문장" : "form", "출전" : "metadata", "어절" : "form", "단어" : "form"}

        self.list_for_data = []
        self.list_for_data.clear()

        self.table.setItem(r, COL_SERIAL_NUMBER, QTableWidgetItem("{0}".format(r)))
        self.list_for_data.append(r)

        if type == True:
            for keywords in SELECTED_CATEGORIES:    # 어쨌든 for문이 2번 돌아가는 거 아닌가..?
                if keywords == "문장":
                    key = dic_t[keywords]
                    if "어절" in SELECTED_CATEGORIES:
                        self.table.setItem(r, COL_SENTENCE, QTableWidgetItem(CURRENT_CONTENTS.sentenceType_soundBlockChecked_sentence_result[r][key]))
                    else:
                        self.table.setItem(r, COL_SENTENCE, QTableWidgetItem(CURRENT_CONTENTS.sentenceType_sentence_result[r][key]))
                if keywords == "단어":
                    key = dic_t[keywords]
                    if "어절" in SELECTED_CATEGORIES:
                        if CURRENT_CONTENTS.sentenceType_word_result_with_soundBlock[r] == "":
                            self.table.setItem(r, COL_WORD, QTableWidgetItem(""))
                        else:
                            self.table.setItem(r, COL_WORD, QTableWidgetItem(CURRENT_CONTENTS.sentenceType_word_result_with_soundBlock[r][key]))

                    else:
                        self.table.setItem(r, COL_WORD, QTableWidgetItem(CURRENT_CONTENTS.sentenceType_word_result[r][key]))
                if keywords == "어절":
                    key = dic_t[keywords]
                    if CURRENT_CONTENTS.sentenceType_soundBlock_result[r] == None:
                        self.table.setItem(r, COL_WORDBLOCK, QTableWidgetItem(""))
                    self.table.setItem(r, COL_WORDBLOCK, QTableWidgetItem(CURRENT_CONTENTS.sentenceType_soundBlock_result[r][key] ))
                if keywords == "출전":
                    key = dic_t[keywords]
                    if "어절" in SELECTED_CATEGORIES:
                        if CURRENT_CONTENTS.sentenceType_soundBlockChecked_origin_result[r][key]["title"] == "":
                            self.table.setItem(r, COL_ORIGIN, QTableWidgetItem(CURRENT_CONTENTS.sentenceType_soundBlockChecked_origin_result[r][key]["publisher"]))
                        else:
                            self.table.setItem(r, COL_ORIGIN, QTableWidgetItem(CURRENT_CONTENTS.sentenceType_soundBlockChecked_origin_result[r][key]["title"]))
                    else:
                        if CURRENT_CONTENTS.sentenceType_origin_result[r][key]["title"] == "":
                            self.table.setItem(r, COL_ORIGIN, QTableWidgetItem(CURRENT_CONTENTS.sentenceType_origin_result[r][key]["publisher"]))
                        else:
                            self.table.setItem(r, COL_ORIGIN, QTableWidgetItem(CURRENT_CONTENTS.sentenceType_origin_result[r][key]["title"]))

        else:
            for keywords in SELECTED_CATEGORIES:    # 어쨌든 for문이 2번 돌아가는 거 아닌가..?
                if keywords == "문장":
                    key = dic_t[keywords]
                
                    if "어절" in SELECTED_CATEGORIES:
                        if CURRENT_CONTENTS.paragraphType_soundBlockChecked_sentence_result[r][key][0] == '“' or CURRENT_CONTENTS.paragraphType_soundBlockChecked_sentence_result[r][key][0] == "‘" or CURRENT_CONTENTS.paragraphType_soundBlockChecked_sentence_result[r][key][0] == "[" or CURRENT_CONTENTS.paragraphType_soundBlockChecked_sentence_result[r][key][0] == "." or CURRENT_CONTENTS.paragraphType_soundBlockChecked_sentence_result[r][key][0] == " ":
                            self.table.setItem(r, COL_SENTENCE, QTableWidgetItem(CURRENT_CONTENTS.paragraphType_soundBlockChecked_sentence_result[r][key][1:]))
                            self.list_for_data.append(CURRENT_CONTENTS.paragraphType_soundBlockChecked_sentence_result[r][key][1:])
                        else:
                            self.table.setItem(r, COL_SENTENCE, QTableWidgetItem(CURRENT_CONTENTS.paragraphType_soundBlockChecked_sentence_result[r][key]))
                            self.list_for_data.append(CURRENT_CONTENTS.paragraphType_soundBlockChecked_sentence_result[r][key])

                    else:
                        if CURRENT_CONTENTS.paragraphType_sentence_result[r][key][0] == '“' or CURRENT_CONTENTS.paragraphType_sentence_result[r][key][0] == "‘" or CURRENT_CONTENTS.paragraphType_sentence_result[r][key][0] == "[" or CURRENT_CONTENTS.paragraphType_sentence_result[r][key][0] == "." or CURRENT_CONTENTS.paragraphType_sentence_result[r][key][0] == " ":
                            self.table.setItem(r, COL_SENTENCE, QTableWidgetItem(CURRENT_CONTENTS.paragraphType_sentence_result[r][key][1:]))
                            self.list_for_data.append(CURRENT_CONTENTS.paragraphType_sentence_result[r][key][1:])
                        else:
                            self.table.setItem(r, COL_SENTENCE, QTableWidgetItem(CURRENT_CONTENTS.paragraphType_sentence_result[r][key]))
                            self.list_for_data.append(CURRENT_CONTENTS.paragraphType_sentence_result[r][key])

                if keywords == "단어":
                    if "어절" in SELECTED_CATEGORIES:
                        if CURRENT_CONTENTS.paragraphType_word_result_with_soundBlock[r] == "":
                            self.table.setItem(r, COL_WORD, QTableWidgetItem(""))
                            self.list_for_data.append("")
                        else:
                            self.table.setItem(r, COL_WORD, QTableWidgetItem(CURRENT_CONTENTS.paragraphType_word_result_with_soundBlock[r]))
                            self.list_for_data.append(CURRENT_CONTENTS.paragraphType_word_result_with_soundBlock[r])

                    else:
                        self.table.setItem(r, COL_WORD, QTableWidgetItem(CURRENT_CONTENTS.paragraphType_word_result[r]))
                        self.list_for_data.append(CURRENT_CONTENTS.paragraphType_word_result[r])

                if keywords == "어절":
                    self.table.setItem(r, COL_WORDBLOCK, QTableWidgetItem(CURRENT_CONTENTS.paragraphType_soundBlock_result[r]))
                    self.list_for_data.append(CURRENT_CONTENTS.paragraphType_soundBlock_result[r])

                if keywords == "출전":
                    key = dic_t[keywords]
                    if "어절" in SELECTED_CATEGORIES:
                        if CURRENT_CONTENTS.paragraphType_soundBlockChecked_origin_result[r][key]["title"] == "":
                            self.table.setItem(r, COL_ORIGIN, QTableWidgetItem(CURRENT_CONTENTS.paragraphType_soundBlockChecked_origin_result[r][key]["publisher"]))
                            self.list_for_data.append(CURRENT_CONTENTS.paragraphType_soundBlockChecked_origin_result[r][key]["publisher"])
                        else:
                            self.table.setItem(r, COL_ORIGIN, QTableWidgetItem(CURRENT_CONTENTS.paragraphType_soundBlockChecked_origin_result[r][key]["title"]))
                            self.list_for_data.append(CURRENT_CONTENTS.paragraphType_soundBlockChecked_origin_result[r][key]["title"])
                    else:
                        if CURRENT_CONTENTS.paragraphType_origin_result[r][key]["title"] == "":
                            self.table.setItem(r, COL_ORIGIN, QTableWidgetItem(CURRENT_CONTENTS.paragraphType_origin_result[r][key]["publisher"]))
                            self.list_for_data.append(CURRENT_CONTENTS.paragraphType_origin_result[r][key]["publisher"])
                        else:
                            self.table.setItem(r, COL_ORIGIN, QTableWidgetItem(CURRENT_CONTENTS.paragraphType_origin_result[r][key]["title"]))
                            self.list_for_data.append(CURRENT_CONTENTS.paragraphType_origin_result[r][key]["title"])

            self.list_for_sequence.append(self.list_for_data)


    def searchData(self):
        global ROW_SIZE
        global COL_SIZE
        global CURRENT_CONTENTS # Parsed data
        global SELECTED_CATEGORIES
        global SEARCH_ALL

        CURRENT_CONTENTS = None
        CURRENT_CONTENTS = Parsing(self.parent.myObjectFile, self.ln.text())

        self.wipeTableData()
        self.list_for_sequence = []
        self.list_for_sequence.clear()
        

        try:
            if CURRENT_CONTENTS.fileType == True:
                if SEARCH_ALL == True:
                    self.changeStatusBar()

                    if "어절" in SELECTED_CATEGORIES:
                        ROW_SIZE = CURRENT_CONTENTS.sentenceType_soundBlock_result_count + 1
                    else:
                        ROW_SIZE = CURRENT_CONTENTS.sentenceType_word_result_count + 1

                    self.reAppendTable()
                    if ROW_SIZE:
                        for r in range(1, ROW_SIZE, 1):   # ROW_SIZE 만큼만 출력
                            self.printSearchResultData(r, True)

                self.changeStatusBar()
                if (ROW_SIZE >= CURRENT_CONTENTS.sentenceType_soundBlock_result_count) and (SEARCH_ALL == False):    # 결과의 갯수와 ROW_SIZE 비교
                    for r in range(1, CURRENT_CONTENTS.sentenceType_soundBlock_result_count + 1, 1):   # ROW_SIZE 만큼만 출력
                        self.printSearchResultData(r, True)


                if (ROW_SIZE < CURRENT_CONTENTS.sentenceType_soundBlock_result_count) and (SEARCH_ALL == False):
                    for r in range(1, ROW_SIZE, 1):   # ROW_SIZE 만큼만 출력
                        self.printSearchResultData(r, True)
            
            else:
                if SEARCH_ALL == True:
                    self.changeStatusBar()

                    if "어절" in SELECTED_CATEGORIES:
                        ROW_SIZE = CURRENT_CONTENTS.paragraphType_soundBlock_result_count + 1
                    else:
                        ROW_SIZE = CURRENT_CONTENTS.paragraphType_word_result_count + 1

                    self.reAppendTable()
                    if ROW_SIZE:
                        for r in range(1, ROW_SIZE, 1):   # ROW_SIZE 만큼만 출력
                            self.printSearchResultData(r, False)

                self.changeStatusBar()
                if (ROW_SIZE >= CURRENT_CONTENTS.paragraphType_soundBlock_result_count) and (SEARCH_ALL == False):    # 결과의 갯수와 ROW_SIZE 비교
                    for r in range(1, CURRENT_CONTENTS.paragraphType_soundBlock_result_count + 1, 1):   # ROW_SIZE 만큼만 출력
                        self.printSearchResultData(r, False)


                if (ROW_SIZE < CURRENT_CONTENTS.paragraphType_soundBlock_result_count) and (SEARCH_ALL == False):
                    for r in range(1, ROW_SIZE, 1):   # ROW_SIZE 만큼만 출력
                        self.printSearchResultData(r, False)


                    
        except error:
            self.wipeTableData()


