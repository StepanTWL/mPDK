import sys
from PyQt5 import QtWidgets
from Tests.frame import Ui_Dialog

app = QtWidgets.QApplication(sys.argv)
ResistorCalculator = QtWidgets.QMainWindow()
ui = Ui_Dialog()
ui.setupUi(ResistorCalculator)
ResistorCalculator.show()
sys.exit(app.exec_())