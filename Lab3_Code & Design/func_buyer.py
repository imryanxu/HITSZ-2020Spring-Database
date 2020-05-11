import pymysql
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from buyerUI import Ui_MainWindow


class buyerUI(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self, db, cursor, buyer_no):
        super(buyerUI, self).__init__()
        self.setupUi(self)

        self.db = db
        self.cursor = cursor
        self.buyer_no = buyer_no

        self.commodityTable.setColumnCount(6)
        self.commodityTable.setHorizontalHeaderLabels(["商品编号", "商店编号", "商品名称", "价格", "折扣", "描述"])
        self.commodityTable.resizeRowsToContents()
        self.commodityTable.setColumnWidth(0, 90)
        self.commodityTable.setColumnWidth(1, 90)
        self.commodityTable.setColumnWidth(2, 150)
        self.commodityTable.setColumnWidth(3, 70)
        self.commodityTable.setColumnWidth(4, 70)
        self.commodityTable.setColumnWidth(5, 250)

        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["商品编号", "商店编号", "商品名称", "价格", "折扣", "数量"])
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 100)

        self.showBuyerInfo()
        self.setCommodityTable()

        self.showcartButton.clicked.connect(self.showcart)
        self.addButton.clicked.connect(self.addcart)
        self.deleteButton.clicked.connect(self.deletecart)
        self.updateButton.clicked.connect(self.updatecart)

    def dataToTableWidget(self, data):
        self.tableWidget.setRowCount(len(data))
        for i in range(0, len(data)):
            for j in range(0, 6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data[i][j])))

    def dataTocommodityTable(self, data):
        self.commodityTable.setRowCount(len(data))
        for i in range(0, len(data)):
            for j in range(0, 6):
                self.commodityTable.setItem(i, j, QTableWidgetItem(str(data[i][j])))

    def showBuyerInfo(self):
        self.sql = 'select buyer_no, b_name, b_sex, b_tel, rep from buyer where buyer_no = \"' \
                   + self.buyer_no + '\";'
        self.cursor.execute(self.sql)
        self.buyerInfo = self.cursor.fetchone()

        self.InfousernoLabel.setText(self.buyerInfo[0])
        self.InfonameLabel.setText(self.buyerInfo[1])
        self.InfosexLabel.setText(self.buyerInfo[2])
        self.InfotelLabel.setText(self.buyerInfo[3])
        self.repLabel.setText(str(self.buyerInfo[4]) + '星信誉度')

    def setCommodityTable(self):
        self.sql = 'select * from commodity;'
        self.cursor.execute(self.sql)
        self.commodityInfo = self.cursor.fetchall()
        self.dataTocommodityTable(self.commodityInfo)

    def showcart(self):
        self.sql = 'select cart.c_no, commodity.shop_no, commodity.c_name, commodity.price, \
commodity.off, cart.cartnum from cart, commodity where cart.c_no = \
commodity.c_no and cart.buyer_no = \"' + self.buyer_no + '\";'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.cartInfo = self.cursor.fetchall()
        self.dataToTableWidget(self.cartInfo)

    def addcart(self):
        if self.selectLine.text() == '':
            QtWidgets.QMessageBox.warning(self, 'Warning', '商品编号不能为空！')
        else:
            self.sql = 'select * from cart where c_no =\"' + self.selectLine.text() \
+ '\" and buyer_no = \"' + self.buyer_no + '\";'
            print(self.sql)
            self.cursor.execute(self.sql)
            self.data = self.cursor.fetchone()
            if self.data is not None:
                QtWidgets.QMessageBox.warning(self, 'Warning', '已存在该商品编号，请使用"更新购物车"！')
            else:
                self.sql = 'insert into cart values (\"' + self.buyer_no + '\", \"' + self.selectLine.text() \
+ '\", ' + self.cartnumLine.text() + ');'
                print(self.sql)
                self.cursor.execute(self.sql)
                QtWidgets.QMessageBox.information(self, 'Information', '已加入购物车')
                self.db.commit()
                self.selectLine.clear()
                self.cartnumLine.clear()

    def deletecart(self):
        self.sql = 'select * from cart where c_no =\"' + self.selectLine.text() \
+ '\" and buyer_no = \"' + self.buyer_no + '\";'
        self.cursor.execute(self.sql)
        self.data = self.cursor.fetchone()
        if self.data is None:
            QtWidgets.QMessageBox.warning(self, 'Warning', '购物车中无该商品！删除失败！')
        else:
            self.sql = 'delete from cart where c_no =\"' + self.selectLine.text() \
+ '\" and buyer_no = \"' + self.buyer_no + '\";'
            self.cursor.execute(self.sql)
            QtWidgets.QMessageBox.information(self, 'Information', '已删除该商品！')
            self.db.commit()
            self.selectLine.clear()
            self.cartnumLine.clear()

    def updatecart(self):
        self.sql = 'update cart set cartnum = \"' + self.cartnumLine.text() + '\" where c_no =\"' + self.selectLine.text() \
+ '\" and buyer_no = \"' + self.buyer_no + '\";'
        self.cursor.execute(self.sql)
        QtWidgets.QMessageBox.information(self, 'Information', '已更新！')
        self.db.commit()
        self.selectLine.clear()
        self.cartnumLine.clear()


if __name__ == "__main__":
    db = pymysql.connect(host="localhost", user="root", password="HelloSQL", database="mis")
    cursor = db.cursor()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    buyerUI = buyerUI(db, cursor, "B001")
    buyerUI.show()
    sys.exit(app.exec_())
