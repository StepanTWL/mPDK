import sys

from PyQt5 import QtWidgets
from main import main


def on_click_new():
    main.ResistFormula.setText('')
    main.Result.setText(f'Result    0Ω')
    main.radioButtonResistor.setChecked(True)
    main.radioButtonSymbol1.setChecked(True)


def on_click_save():
    file, check = QtWidgets.QFileDialog.getSaveFileName(None, 'Save file', 'c:\\', "JSON Files (*.json);;All Files (*)")

    if check:
        with open(file, "w") as file:
            pass



def on_click_open():
    file, check = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', 'c:\\', "JSON Files (*.json);;All Files (*)")

    if check:
        with open(file, "r") as file:
            pass

if __name__ == '__main__':
    main.actionNew.triggered.connect(on_click_new)
    main.actionSave.triggered.connect(on_click_save)
    main.actionOpen.triggered.connect(on_click_open)
    main.actionExit.triggered.connect(sys.exit)