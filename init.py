import sys
from app import MyApp
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)    # 어플리케이션 객체를 생성
w = MyApp()

sys.exit(app.exec_())           # app.exec_()는 이벤트 처리를 위한 루프, 창을 종료하면 루프 종료, sys.exit() 실행