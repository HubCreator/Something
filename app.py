from PyQt5 import QtWidgets
from layout import MyLayout
from PyQt5.QtCore import  QCoreApplication, QStringListModel
from PyQt5.QtWidgets import QAction, QFileDialog, QMainWindow, QMenu, QMessageBox

class MyApp(QMainWindow):                       # QMainWindow 클래스 상속
    def __init__(self, parent = None):                         # 생성자
        super(MyApp, self).__init__()           # 상위 객체 생성(QMainWindow 생성자 호출)
        self.main_widget = MyLayout(self)
        self.setCentralWidget(self.main_widget)
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(600, 300, 800, 600)    # 창이 뜨는 위치와 크기 조절
        self.setWindowTitle('말뭉치 단어 찾기 프로그램')

        self.myStatusBar = self.statusBar()
        self.myStatusBar.showMessage('hello')

        
        self.makeMenuBar()

        self.show()

        # self.open_dialog_box()
        self.myObject = self.getOpenFilesAndDirs()
        # print(self.myObject)


    def makeMenuBar(self):
        obj = self.menuBar()
        self.menuBar_file = obj.addMenu('File')     # 메뉴 바 내의 그룹 생성
        self.menuBar_edit = obj.addMenu('Edit')

        self.menuBar_file_exit = QAction('Exit', self)       # 메뉴 객체 생성
        self.menuBar_file_exit.setShortcut('Ctrl+Q')
        self.menuBar_file_exit.setStatusTip('누르면... 안녕')
        self.menuBar_file_exit.triggered.connect(QCoreApplication.instance().quit)

        self.menuBar_file_new = QMenu('New', self)

        self.menuBar_file_new_newFile = QAction('새로운 파일 열기', self)
        self.menuBar_file_new_openFile = QAction('검색 대상 파일 선택하기..', self)

        self.menuBar_file_new_openFile.triggered.connect(self.pushButton_handler)

        self.menuBar_file_new.addAction(self.menuBar_file_new_newFile) # 서브 메뉴 등록
        self.menuBar_file_new.addAction(self.menuBar_file_new_openFile)

        self.menuBar_file.addMenu(self.menuBar_file_new)
        self.menuBar_file.addAction(self.menuBar_file_exit)          # 메뉴 등록

    def pushButton_handler(self):
        # self.open_dialog_box()
        self.getOpenFilesAndDirs()

    # def open_dialog_box(self):
    #     self.filename = QFileDialog.getOpenFileNames()
    #     self.path = self.filename[0]
    #     print(self.path)
    #     self.dataFile = "languageData"
    #     self.ext = ".json"
    #     self.myObjectFile = self.path[self.path.find(self.dataFile) : self.path.find(self.ext) + len(self.ext)]

    def closeEvent(self, QCloseEvent):
        answer = QMessageBox.question(self, '종료 확인', '종료하시겠습니까??', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if answer == QMessageBox.Yes:
            QCloseEvent.accept()
        elif answer == QMessageBox.No:
            QCloseEvent.ignore()

    def getOpenFilesAndDirs(parent=None, caption='파일 혹은 폴더 지정', directory='', filter='*.json', initialFilter='', options=None):
        # def updateText():
        #     # update the contents of the line edit widget with the selected files
        #     selected = []
        #     for index in view.selectionModel().selectedRows():
        #         selected.append('"{}"'.format(index.data()))
        #     lineEdit.setText(' '.join(selected))

        dialog = QtWidgets.QFileDialog(parent, windowTitle=caption)
        dialog.setFileMode(dialog.ExistingFiles)
        if options:
            dialog.setOptions(options)
        dialog.setOption(dialog.DontUseNativeDialog, True)
        if directory:
            dialog.setDirectory(directory)
        if filter:
            dialog.setNameFilter(filter)
            if initialFilter:
                dialog.selectNameFilter(initialFilter)

        # by default, if a directory is opened in file listing mode, 
        # QFileDialog.accept() shows the contents of that directory, but we 
        # need to be able to "open" directories as we can do with files, so we 
        # just override accept() with the default QDialog implementation which 
        # will just return exec_()
        dialog.accept = lambda: QtWidgets.QDialog.accept(dialog)

        # there are many item views in a non-native dialog, but the ones displaying 
        # the actual contents are created inside a QStackedWidget; they are a 
        # QTreeView and a QListView, and the tree is only used when the 
        # viewMode is set to QFileDialog.Details, which is not this case
        stackedWidget = dialog.findChild(QtWidgets.QStackedWidget)
        view = stackedWidget.findChild(QtWidgets.QListView)
        # view.selectionModel().selectionChanged.connect(updateText)

        # lineEdit = dialog.findChild(QtWidgets.QLineEdit)
        # clear the line edit contents whenever the current directory changes
        # dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

        dialog.exec_()
        return dialog.selectedFiles()