import sqlite3

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('coffee.ui', self)  # загрузка дизайна
        self.entry.clicked.connect(self.do_entry)
        self.statistics.clicked.connect(self.stats)

    def do_entry(self):
        con = sqlite3.connect('coffee.db')  # создание/соединение с бд
        cur = con.cursor()  # создание курсора
        cur.execute("""CREATE TABLE IF NOT EXISTS revenue(
                           volume FLOAT,
                           price INT,
                           date DATE);
                           """)  # создание таблицы
        vol = self.volume.text()
        pr = self.price.text()
        dt = self.date.text()
        ins = (vol, pr, dt)
        con.execute("""INSERT INTO revenue(?, ?, ?)""", ins)
        con.commit()  # сохранение изменений

    def stats(self):
        con = sqlite3.connect('coffee.db')  # создание/соединение с бд
        cur = con.cursor()  # создание курсора
        cur.execute("""CREATE TABLE IF NOT EXISTS revenue(
                           volume FLOAT,
                           price INT,
                           date DATE);
                           """)  # создание таблицы
        summoney = cur.execute("""SELECT SUM(price) FROM revenue""").fetchone()
        summoney = list(summoney)[0]
        print(summoney)
        dates = cur.execute("""SELECT date FROM revenue""").fetchall()
        dates = list(set(dates))
        moneylist = []
        for i in dates:
            money = cur.execute("""SELECT SUM(price) FROM revenue
                                  WHERE date = ?""", i).fetchone()
            money = list(money)[0]
            moneylist.append(money)
        print(max(moneylist))
        print(min(moneylist))
        con.commit()  # сохранение изменений


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
