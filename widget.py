import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class Exam(QWidget):            # QWidget 클래스 상속
    def __init__(self):         # 생성자
        super().__init__()      # 상위 객체 생성(QWidget 생성자 호출)
        self.initUI()
    def initUI(self):
        btn = QPushButton('hi', self)
        btn.resize(btn.sizeHint())
        btn.setToolTip('tooltip')
        btn.move(20, 30)

        self.setGeometry(300, 300, 400, 500)    # 창이 뜨는 위치와 크기 조절
        self.setWindowTitle('myFirst project with python')

        self.show()

app = QApplication(sys.argv)    # 어플리케이션 객체를 생성
w = Exam()
sys.exit(app.exec_())           # app.exec_()는 이벤트 처리를 위한 루프, 창을 종료하면 루프 종료, sys.exit() 실행