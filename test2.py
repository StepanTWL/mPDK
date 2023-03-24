import datetime
import time

from PyQt5 import uic, QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget, QApplication


class WeatherData(QThread):
    req = weather.today()
    temp = req['temp']
    feels = req['feels']
    pres = req['pressure']
    speed = str(req['wind']['speed'])
    city = req['city']
    type = req['dis']

    week = weather.week()

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        while True:
            try:
                req = weather.today()
            except:
                req['temp'] = self.temp
                req['feels'] = self.feels
                req['pressure'] = self.pres
                req['wind']['speed'] = self.speed
                req['city'] = self.city
                req['dis'] = self.type

            try:
                req_week = weather.week()
                self.week = req_week
            except:
                self.week = DAYS
            self.temp = req['temp']
            self.feels = req['feels']
            self.pres = req['pressure']
            self.speed = str(req['wind']['speed'])
            self.city = req['city']
            self.type = req['dis']
            print('RUN', self.temp)
            time.sleep(3)

class App(QWidget):
    tic = False
    def __init__(self):
        QWidget.__init__(self)
        self.weather = WeatherData()
        self.weather.start()
        self.set()
        self.setData()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.setData)
        self.timer.start(1000)

    def set(self):
        self.w_root = uic.loadUi('root.ui')
        self.w_root.btn_more.clicked.connect(self.setHeight)
        self.w_root.show()

    def setData(self):
        self.w_root.l_temp.setText(str(self.weather.temp) + 'C')
        self.w_root.l_feel.setText(self.weather.feels)
        self.w_root.l_pres.setText(self.weather.pres)
        self.w_root.l_wind.setText(self.weather.speed + 'm/s')
        self.w_root.l_city.setText(self.weather.city)
        self.w_root.l_type.setText(self.weather.type)

        today = DAYS[datetime.datetime.today().weekday()]
        self.w_root.l_day.setText(today['title'])
        color = today['color']
        self.w_root.l_day.setStyleSheet(f'color:{color}')

        if self.tic:
            now = datetime.datetime.today().strftime("%H:%M:%S")
            self.tic = False
        else:
            now = datetime.datetime.today().strftime("%H %M %S")
            self.tic = True
        self.w_root.l_time.setText(now)

    def setHeight(self):
        print('Hello')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()