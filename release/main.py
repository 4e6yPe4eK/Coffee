import sqlite3
import sys
from PyQt5 import QtWidgets, QtCore
from addEditCoffeeFormUi import addEditCoffeeFormUi
from mainUi import mainUi


class AddEditForm(addEditCoffeeFormUi):
    def __init__(self, par, tp, data=None):
        super().__init__()
        self.tp = tp
        self.par = par
        self.data = data
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.setupUi()

    def setupUi(self):
        if self.tp:
            self.setWindowTitle('Изменить')
            self.pushButton.setText('Изменить')
            self.num = int(self.data[0])
            self.wtitle.setText(self.data[1])
            self.wdegree.setText(self.data[2])
            self.wtype.setText(self.data[3])
            self.wtaste.setText(self.data[4])
            self.wprice.setValue(int(self.data[5]))
            self.wamount.setValue(int(self.data[6]))
            self.pushButton.clicked.connect(self.edit)
        else:
            self.setWindowTitle('Добавить')
            self.pushButton.setText('Добавить')
            self.pushButton.clicked.connect(self.add)

    def add(self):
        self.cur.execute("INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?)",
                         (None,
                          self.wtitle.text(),
                          self.wdegree.text(),
                          self.wtype.text(),
                          self.wtaste.text(),
                          self.wprice.value(),
                          self.wamount.value()))
        self.con.commit()
        self.par.loadTable()
        self.par.ui = None

    def edit(self):
        self.cur.execute("UPDATE coffee SET "
                         "title = ?, "
                         "degree = ?, "
                         "type = ?, "
                         "taste = ?, "
                         "price = ?, "
                         "amount = ? "
                         "WHERE id = ?",
                         (self.wtitle.text(),
                          self.wdegree.text(),
                          self.wtype.text(),
                          self.wtaste.text(),
                          self.wprice.value(),
                          self.wamount.value(),
                          self.num))

        self.con.commit()
        self.par.loadTable()
        self.par.ui = None


class Main(mainUi):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Эспрессо")
        self.pushButton.clicked.connect(self.add)
        self.loadTable()

    def loadTable(self):
        data = list(self.cur.execute("SELECT * FROM coffee"))
        self.tableWidget.doubleClicked.connect(self.edit)
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
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, item)

    def edit(self, ind):
        self.ui = None
        i = ind.row()
        data = []
        for j in range(7):
            data.append(self.tableWidget.item(i, j).text())
        self.ui = AddEditForm(self, True, data)
        self.ui.show()

    def add(self):
        self.ui = AddEditForm(self, False)
        self.ui.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    interface = Main()
    interface.show()
    sys.exit(app.exec_())
