import pymysql
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from adminUI import Ui_MainWindow


class adminUI(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self, db, cursor, admin_no):
        super(adminUI, self).__init__()
        self.setupUi(self)

        self.db = db
        self.cursor = cursor
        self.admin_no = admin_no

        self.sellerTable.setColumnCount(4)
        self.sellerTable.setHorizontalHeaderLabels(["卖家编号", "卖家姓名", "卖家性别", "联系电话"])
        self.sellerTable.resizeRowsToContents()
        self.sellerTable.setColumnWidth(0, 100)
        self.sellerTable.setColumnWidth(1, 100)
        self.sellerTable.setColumnWidth(2, 100)
        self.sellerTable.setColumnWidth(3, 200)

        self.buyerTable.setColumnCount(4)
        self.buyerTable.setHorizontalHeaderLabels(["买家编号", "买家姓名", "买家性别", "联系电话"])
        self.buyerTable.resizeRowsToContents()
        self.buyerTable.setColumnWidth(0, 100)
        self.buyerTable.setColumnWidth(1, 100)
        self.buyerTable.setColumnWidth(2, 100)
        self.buyerTable.setColumnWidth(3, 200)

        self.showAdminInfo()
        self.setsellerTable()
        self.setbuyerTable()

        self.adduserButton.clicked.connect(self.adduser)
        self.deleteuserButton.clicked.connect(self.deleteuser)
        self.updateuserButton.clicked.connect(self.updateuser)
        self.selectuserButton.clicked.connect(self.selectuser)

    def dataTobuyerTable(self, data):
        self.buyerTable.setRowCount(len(data))
        for i in range(0, len(data)):
            for j in range(0, 4):
                self.buyerTable.setItem(i, j, QTableWidgetItem(str(data[i][j])))

    def dataTosellerTable(self, data):
        self.sellerTable.setRowCount(len(data))
        for i in range(0, len(data)):
            for j in range(0, 4):
                self.sellerTable.setItem(i, j, QTableWidgetItem(str(data[i][j])))

    def showAdminInfo(self):
        self.sql = 'select * from admin where admin_no = \"' + self.admin_no + '\";'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.sellerInfo = self.cursor.fetchone()

        self.adminnolabel.setText(self.sellerInfo[0])
        self.adminnamelabel.setText(self.sellerInfo[1])
        self.adminsexlabel.setText(self.sellerInfo[2])
        self.admintellabel.setText(self.sellerInfo[3])

    def setsellerTable(self):
        self.sql = 'select seller_no, s_name, s_sex, s_tel from seller'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.sellerInfo = self.cursor.fetchall()
        self.dataTosellerTable(self.sellerInfo)

    def setbuyerTable(self):
        self.sql = 'select buyer_no, b_name, b_sex, b_tel from buyer'
        print(self.sql)
        self.cursor.execute(self.sql)
        self.buyerInfo = self.cursor.fetchall()
        self.dataTobuyerTable(self.buyerInfo)

    def adduser(self):
        self.nocheckBox.setCheckState(True)
        self.sexcheckBox.setCheckState(True)
        self.namecheckBox.setCheckState(True)
        self.telcheckBox.setCheckState(True)
        if self.buyerradioButton.isChecked():
            self.sql = 'select * from buyer where buyer_no =\"' + self.noLine.text() + '\"'
            self.cursor.execute(self.sql)
            self.data = self.cursor.fetchone()
            if self.data is not None:
                QtWidgets.QMessageBox.warning(self, 'Warning', '买家编号已存在！')
            elif self.sexLine.text() != '男' and self.sexLine.text() != '女':
                QtWidgets.QMessageBox.information(self, 'Information', '请填写"男"或"女"！')
            else:
                self.sql = 'insert into buyer values (\"' + self.noLine.text() + '\", \"' + self.nameLine.text() \
+ '\", \"' + self.sexLine.text() + '\", \"' + self.telLine.text() + '\",null)'
                print(self.sql)
                self.cursor.execute(self.sql)
                self.db.commit()
                self.setbuyerTable()
                self.nocheckBox.setCheckState(False)
                self.sexcheckBox.setCheckState(False)
                self.namecheckBox.setCheckState(False)
                self.telcheckBox.setCheckState(False)

        elif self.sellerradioButton.isChecked():
            self.sql = 'select * from seller where seller_no =\"' + self.noLine.text() + '\"'
            self.cursor.execute(self.sql)
            self.data = self.cursor.fetchone()
            if self.data is not None:
                QtWidgets.QMessageBox.warning(self, 'Warning', '卖家编号已存在！')
            elif self.sexLine.text() != '男' and self.sexLine.text() != '女':
                QtWidgets.QMessageBox.information(self, 'Information', '请填写"男"或"女"！')
            else:
                self.sql = 'insert into seller values (\"' + self.noLine.text() + '\",null, \"' + self.nameLine.text() \
                           + '\", \"' + self.sexLine.text() + '\", \"' + self.telLine.text() + '\")'
                print(self.sql)
                self.cursor.execute(self.sql)
                self.db.commit()
                self.setsellerTable()
                self.nocheckBox.setCheckState(False)
                self.sexcheckBox.setCheckState(False)
                self.namecheckBox.setCheckState(False)
                self.telcheckBox.setCheckState(False)
        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', '需要选择角色！')

    def deleteuser(self):
        self.nocheckBox.setCheckState(True)
        if self.buyerradioButton.isChecked():
            self.sql = 'select * from buyer where buyer_no =\"' + self.noLine.text() + '\"'
            self.cursor.execute(self.sql)
            self.data = self.cursor.fetchone()
            if self.data is None:
                QtWidgets.QMessageBox.warning(self, 'Warning', '要删除的买家编号不存在！')
            else:
                self.sql = 'delete from buyer where buyer_no= \"' + self.noLine.text() + '\"'
                print(self.sql)
                self.cursor.execute(self.sql)
                self.db.commit()
                self.setbuyerTable()
                self.nocheckBox.setCheckState(False)

        elif self.sellerradioButton.isChecked():
            self.sql = 'select * from seller where seller_no =\"' + self.noLine.text() + '\"'
            self.cursor.execute(self.sql)
            self.data = self.cursor.fetchone()
            if self.data is None:
                QtWidgets.QMessageBox.warning(self, 'Warning', '要删除的卖家编号不存在！')
            else:
                self.sql = 'delete from seller where seller_no = \"' + self.noLine.text() + '\"'
                print(self.sql)
                self.cursor.execute(self.sql)
                self.db.commit()
                self.setsellerTable()
                self.nocheckBox.setCheckState(False)
        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', '需要选择角色！')

    def updateuser(self):
        self.nocheckBox.setCheckState(True)
        if self.buyerradioButton.isChecked():
            self.sql = 'select * from buyer where buyer_no =\"' + self.noLine.text() + '\"'
            self.cursor.execute(self.sql)
            self.data = self.cursor.fetchone()
            if self.data is None:
                QtWidgets.QMessageBox.warning(self, 'Warning', '要更新的买家编号不存在！')
            else:
                self.sql = 'update buyer set b_tel = \"' + self.telLine.text() + '\" where buyer_no =\"' + self.noLine.text() + '\"'
                print(self.sql)
                self.cursor.execute(self.sql)
                self.db.commit()
                self.setbuyerTable()
                self.nocheckBox.setCheckState(False)

        elif self.sellerradioButton.isChecked():
            self.sql = 'select * from seller where seller_no =\"' + self.noLine.text() + '\"'
            self.cursor.execute(self.sql)
            self.data = self.cursor.fetchone()
            if self.data is None:
                QtWidgets.QMessageBox.warning(self, 'Warning', '要更新的卖家编号不存在！')
            else:
                self.sql = 'update seller set s_tel = \"' + self.telLine.text() + '\" where seller_no =\"' + self.noLine.text() + '\"'
                print(self.sql)
                self.cursor.execute(self.sql)
                self.db.commit()
                self.setsellerTable()
                self.nocheckBox.setCheckState(False)
        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', '需要选择角色！')

    def selectuser(self):
        if self.buyerradioButton.isChecked():
            self.sql = 'select buyer_no, b_name, b_sex, b_tel from buyer \
where b_sex =\"' + self.sexLine.text() + '\"'
            print(self.sql)
            self.cursor.execute(self.sql)
            self.buyerInfo = self.cursor.fetchall()
            self.dataTobuyerTable(self.buyerInfo)

        elif self.sellerradioButton.isChecked():
            self.sql = 'select seller_no, s_name, s_sex, s_tel from seller \
where s_name like \"%' + self.nameLine.text() + '%\"'
            self.cursor.execute(self.sql)
            self.sellerInfo = self.cursor.fetchall()
            self.dataTosellerTable(self.sellerInfo)

        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', '需要选择角色！')


if __name__ == "__main__":
    db = pymysql.connect(host="localhost", user="root", password="HelloSQL", database="mis")
    cursor = db.cursor()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    adminUI = adminUI(db, cursor, "A001")
    adminUI.show()
    sys.exit(app.exec_())
