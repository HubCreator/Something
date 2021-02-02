import sys
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QAction, QMenu
from PyQt5.QtCore import QCoreApplication

class Exam(QMainWindow):                        # QWidget 클래스 상속
    def __init__(self):                         # 생성자
        super().__init__()                      # 상위 객체 생성(QWidget 생성자 호출)
        self.initUI()
    def initUI(self):
        self.setGeometry(700, 300, 500, 400)    # 창이 뜨는 위치와 크기 조절
        self.setWindowTitle('말뭉치 단어 찾기 프로그램')
        
        self.statusBar()                        # 상태 표시줄 생성
        # self.statusBar().showMessage('hello')

        menuBar = self.menuBar()                # 메뉴 바 생성
        menuBar_file = menuBar.addMenu('File')     # 메뉴 바 내의 그룹 생성
        menuBar_edit = menuBar.addMenu('Edit')

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

        btn = QPushButton('hi', self)
        btn.resize(btn.sizeHint())
        btn.setToolTip('tooltip')
        btn.move(70, 30)

        btn.clicked.connect(QCoreApplication.instance().quit) # QCoreApplication은 모든 이벤트에 대한 처리를 한다.

        self.show()
    def closeEvent(self, QCloseEvent):
        answer = QMessageBox.question(self, '종료 확인', '종료하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer == QMessageBox.Yes:
            QCloseEvent.accept()
        elif answer == QMessageBox.No:
            QCloseEvent.ignore()


app = QApplication(sys.argv)    # 어플리케이션 객체를 생성
w = Exam()
sys.exit(app.exec_())           # app.exec_()는 이벤트 처리를 위한 루프, 창을 종료하면 루프 종료, sys.exit() 실행