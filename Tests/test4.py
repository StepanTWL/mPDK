import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QPlainTextEdit, QApplication, QWidget, QHBoxLayout


class CustomLineEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super(CustomLineEdit, self).__init__()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__contextMenu)

    def __contextMenu(self):
        self._normalMenu = self.createStandardContextMenu()
        self._addCustomMenuItems(self._normalMenu)
        self._normalMenu.exec_(QtGui.QCursor.pos())

    def _addCustomMenuItems(self, menu):
        menu.addSeparator()
        menu.addAction(u'Test', self.testFunc)

    def testFunc(self):
        print("Call")


class mainwindow(QWidget):
    def __init__(self, parent=None):
        super(mainwindow, self).__init__()
        self.setupgui()

    def setupgui(self):
        self.resize(800, 600)
        self.setWindowTitle('test')
        newLayout = QHBoxLayout()
        qlbl = CustomLineEdit()
        newLayout.addWidget(qlbl)
        self.setLayout(newLayout)
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = mainwindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
