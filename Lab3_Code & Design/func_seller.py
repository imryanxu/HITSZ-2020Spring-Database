import pymysql
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from sellerUI import Ui_MainWindow


class sellerUI(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self, db, cursor, seller_no):
        super(sellerUI, self).__init__()
        self.setupUi(self)

        self.db = db
        self.cursor = cursor
        self.seller_no = seller_no

        self.commodityTable.setColumnCount(5)
        self.commodityTable.setHorizontalHeaderLabels(["商品编号", "商品名称", "价格", "折扣", "描述"])
        self.commodityTable.resizeRowsToContents()
        self.commodityTable.setColumnWidth(0, 100)
        self.commodityTable.setColumnWidth(1, 150)
        self.commodityTable.setColumnWidth(2, 70)
        self.commodityTable.setColumnWidth(3, 70)
        self.commodityTable.setColumnWidth(4, 250)

        self.orderTable.setColumnCount(5)
        self.orderTable.setHorizontalHeaderLabels(["订单编号", "买家编号", "商品编号", "商品名称", "商品数量"])
        self.orderTable.resizeRowsToContents()
        self.orderTable.setColumnWidth(0, 100)
        self.orderTable.setColumnWidth(1, 100)
        self.orderTable.setColumnWidth(2, 100)
        self.orderTable.setColumnWidth(3, 150)
        self.orderTable.setColumnWidth(4, 100)

        self.showSellerInfo()
        self.setCommodityTable()
        self.setorderTable()

        self.addcomButton.clicked.connect(self.addcom)
        self.deletecomButton.clicked.connect(self.deletecom)
        self.updatecomButton.clicked.connect(self.updatecom)
        self.selectcomButton.clicked.connect(self.selectcom)

        self.addorderButton.clicked.connect(self.addorder)
        self.deleteorderButton.clicked.connect(self.deleteorder)
        self.updateorderButton.clicked.connect(self.updateorder)
        self.selectorderButton.clicked.connect(self.selectorder)

    def dataToorderTable(self, data):
        self.orderTable.setRowCount(len(data))
        for i in range(0, len(data)):
            for j in range(0, 5):
                self.orderTable.setItem(i, j, QTableWidgetItem(str(data[i][j])))

    def dataTocommodityTable(self, data):
        self.commodityTable.setRowCount(len(data))
        for i in range(0, len(data)):
            for j in range(0, 5):
                self.commodityTable.setItem(i, j, QTableWidgetItem(str(data[i][j])))

    def showSellerInfo(self):
        self.sql = 'select * from seller where seller_no = \"' + self.seller_no + '\";'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.sellerInfo = self.cursor.fetchone()

        self.Infousernolabel.setText(self.sellerInfo[0])
        self.Infonamelabel.setText(self.sellerInfo[2])
        self.Infosexlabel.setText(self.sellerInfo[3])
        self.Infotellabel.setText(self.sellerInfo[4])
        self.Infoshopnolabel.setText(self.sellerInfo[1])

    def setCommodityTable(self):
        self.sql = 'select c_no, c_name, price, off, text from commodity where shop_no = \"' + self.Infoshopnolabel.text() + '\";'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.commodityInfo = self.cursor.fetchall()
        self.dataTocommodityTable(self.commodityInfo)

    def setorderTable(self):
        self.sql = 'select orders.order_no, orders.buyer_no, contents.c_no, commodity.c_name, contents.ordernum \
from orders, commodity, contents where orders.order_no = contents.order_no and contents.c_no = commodity.c_no \
and orders.shop_no = \"' + self.Infoshopnolabel.text() + '\";'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.orderInfo = self.cursor.fetchall()
        self.dataToorderTable(self.orderInfo)

    def addcom(self):
        self.comnocheckBox.setCheckState(True)
        self.comnamecheckBox.setCheckState(True)
        self.pricecheckBox.setCheckState(True)
        self.sql = 'select * from commodity where shop_no = \"' + self.Infoshopnolabel.text() + '\" and c_no = \"' + self.comnoLine.text() + '\";'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.data = self.cursor.fetchone()
        if self.data is not None:
            QtWidgets.QMessageBox.warning(self, 'Warning', '该商品编号已存在！')
        else:
            self.sql = 'insert into commodity values (\"' + self.comnoLine.text() + '\", \"' + \
self.Infoshopnolabel.text() + '\", \"' + self.comnameLine.text() + '\",' + self.priceLine.text() + ',null,\"' + self.textLine.text() + '\");'
            print(self.sql)
            self.cursor.execute(self.sql)
            self.db.commit()
            self.setCommodityTable()
            self.comnocheckBox.setCheckState(False)
            self.comnamecheckBox.setCheckState(False)
            self.pricecheckBox.setCheckState(False)

    def deletecom(self):
        self.comnocheckBox.setCheckState(True)
        self.sql = 'delete from commodity where c_no = \"' + self.comnoLine.text() + '\"';
        print(self.sql)
        self.cursor.execute(self.sql)
        self.db.commit()
        self.setCommodityTable()
        self.comnocheckBox.setCheckState(False)

    def updatecom(self):
        self.comnocheckBox.setCheckState(True)
        if self.pricecheckBox.isChecked():
            self.sql = 'update commodity set price = ' + self.priceLine.text() + ' where c_no = \"' + self.comnoLine.text() + '\";'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.db.commit()
        self.setCommodityTable()
        self.comnocheckBox.setCheckState(False)

    def selectcom(self):
        if self.comnamecheckBox.isChecked():
            self.sql = 'select c_no, c_name, price, off, text from commodity where shop_no = \"' + \
self.Infoshopnolabel.text() + '\" and c_name like \"%' + self.comnameLine.text() + '%\";'
            print(self.sql)
            self.cursor.execute(self.sql)
            self.commodityInfo = self.cursor.fetchall()
            self.dataTocommodityTable(self.commodityInfo)

    def addorder(self):
        self.ordernocheckBox.setCheckState(True)
        self.cnamecheckBox.setCheckState(True)
        self.buyernocheckBox.setCheckState(True)
        self.ordernumcheckBox.setCheckState(True)
        self.sql = 'select c_no from commodity where c_name = \"' + self.cnameLine.text() + '\"'
        self.cursor.execute(self.sql)
        self.cnotemp = self.cursor.fetchone()[0]
        self.sql = 'insert into contents values (\"' + self.ordernoLine.text() + ',\"' + self.cnotemp + '\",' + self.ordernumLine + ')'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.db.commit()
        self.setorderTable()
        self.ordernocheckBox.setCheckState(False)
        self.cnamecheckBox.setCheckState(False)
        self.buyernocheckBox.setCheckState(False)
        self.ordernumcheckBox.setCheckState(False)

    def deleteorder(self):
        self.ordernocheckBox.setCheckState(True)
        self.sql = 'select * from orders where shop_no = \"' + self.Infoshopnolabel.text() + '\" and order_no = \"' + self.ordernoLine.text() + '\";'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.data = self.cursor.fetchone()
        if self.data is None:
            QtWidgets.QMessageBox.warning(self, 'Warning', '无该编号的订单！')
        else:
            self.sql = 'delete from contents where order_no = \"' + self.ordernoLine.text() + '\"'
            print(self.sql)
            self.cursor.execute(self.sql)
            self.db.commit()
            self.setorderTable()
            self.ordernocheckBox.setCheckState(False)

    def updateorder(self):
        self.ordernocheckBox.setCheckState(True)
        self.cnamecheckBox.setCheckState(True)
        self.sql = 'select c_no from commodity where c_name like \"%' + self.cnameLine.text() + '%\"'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.cnotemp = self.cursor.fetchone()[0]
        self.sql = 'update contents set ordernum = ' + self.ordernumLine.text() + ' where c_no =\"' + \
self.cnotemp +'\" and order_no =\"' + self.ordernoLine.text() + '\"'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.db.commit()
        self.setorderTable()
        self.ordernocheckBox.setCheckState(False)
        self.cnamecheckBox.setCheckState(False)

    def selectorder(self):
        if self.cnamecheckBox.isChecked():
            self.sql = 'select orders.order_no, orders.buyer_no, contents.c_no, commodity.c_name, contents.ordernum \
from orders, commodity, contents where orders.order_no = contents.order_no and contents.c_no = commodity.c_no \
and orders.shop_no = \"' + self.Infoshopnolabel.text() + '\" and commodity.c_name like \"%' + self.cnameLine.text() + '%\";'
            print(self.sql)
            self.cursor.execute(self.sql)
            self.orderInfo = self.cursor.fetchall()
            self.dataToorderTable(self.orderInfo)
            self.cnameLine.clear()


if __name__ == "__main__":
    db = pymysql.connect(host="localhost", user="root", password="HelloSQL", database="mis")
    cursor = db.cursor()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    sellerUI = sellerUI(db, cursor, "S001")
    sellerUI.show()
    sys.exit(app.exec_())
