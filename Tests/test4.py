import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Window'
        self.left = 500
        self.top = 200
        self.width = 300
        self.height = 250
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def contextMenuEvent(self, event) -> None:
        contextMenu = QMenu(self)

        newAction = contextMenu.addAction('New')
        quitAction = contextMenu.addAction('Quit')

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAction:
            self.close()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())