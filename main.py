import sqlite3
import sys
from PyQt5 import QtWidgets, QtCore, uic


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Эспрессо")
        self.loadTable()

    def loadTable(self):
        data = list(self.cur.execute("SELECT * FROM coffee"))
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("ID"))
        self.tableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Напиток"))
        self.tableWidget.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Степень обжарки"))
        self.tableWidget.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Тип"))
        self.tableWidget.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem("Вкус"))
        self.tableWidget.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem("Цена"))
        self.tableWidget.setHorizontalHeaderItem(6, QtWidgets.QTableWidgetItem("Масса"))
        for i in range(len(data)):
            for j in range(7):
                item = QtWidgets.QTableWidgetItem(str(data[i][j]))
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.tableWidget.setItem(i, j, item)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.addLibraryPath("platforms/")
    interface = Main()
    interface.show()
    sys.exit(app.exec_())
