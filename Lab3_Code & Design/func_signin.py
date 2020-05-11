import sys
from PyQt5 import QtWidgets
from login import Ui_Form
from func_buyer import buyerUI
from func_seller import sellerUI
from func_admin import adminUI


class LogIn(QtWidgets.QWidget, Ui_Form):

    def __init__(self, db, cursor):
        super(LogIn, self).__init__()
        self.setupUi(self)

        self.sql = ''
        self.db = db
        self.cursor = cursor

        self.loginpushButton.clicked.connect(self.login)

    def login(self):
        if self.usernoline.text() == '':
            QtWidgets.QMessageBox.warning(self, 'Warning', '用户编号不能为空！')

        if self.buyerButton.isChecked() == False and self.sellerButton.isChecked() == False \
                and self.adminButton.isChecked() == False:
            QtWidgets.QMessageBox.warning(self, 'Warning', '必须勾选一项角色身份！')

        if self.buyerButton.isChecked():
            self.sql = 'select bsa_no, pwd from userinfo where bsa_no = \"' + self.usernoline.text() \
                       + "\" and typeno = 1;"
            self.cursor.execute(self.sql)
            self.data = self.cursor.fetchone()
            if self.data is None:
                QtWidgets.QMessageBox.warning(self, 'Warning', '不存在该买家账户！')
                self.usernoline.clear()
                self.pwdline.clear()
            elif self.data[1] == self.pwdline.text():
                # print("success")
                self.close()
                self.buyerUI = buyerUI(self.db, self.cursor, self.data[0])
                self.buyerUI.show()
            else:
                QtWidgets.QMessageBox.warning(self, 'Warning', '密码错误')

        elif self.sellerButton.isChecked():
            self.sql = 'select bsa_no, pwd from userinfo where bsa_no = \"' + self.usernoline.text() \
                       + "\" and typeno = 2;"
            self.cursor.execute(self.sql)
            self.data = self.cursor.fetchone()
            if self.data is None:
                QtWidgets.QMessageBox.warning(self, 'Warning', '不存在该卖家账户！')
                self.usernoline.clear()
            elif self.data[1] == self.pwdline.text():
                self.close()
                self.sellerUI = sellerUI(self.db, self.cursor, self.data[0])
                self.sellerUI.show()
            else:
                QtWidgets.QMessageBox.warning(self, 'Warning', '密码错误')

        elif self.adminButton.isChecked():
            self.sql = 'select bsa_no, pwd from userinfo where bsa_no = \"' + self.usernoline.text() \
                       + "\" and typeno = 3;"
            self.cursor.execute(self.sql)
            self.data = self.cursor.fetchone()
            if self.data is None:
                QtWidgets.QMessageBox.warning(self, 'Warning', '不存在该管理者账户！')
                self.usernoline.clear()
            elif self.data[1] == self.pwdline.text():
                self.close()
                self.adminUI = adminUI(self.db, self.cursor, self.data[0])
                self.adminUI.show()
            else:
                QtWidgets.QMessageBox.warning(self, 'Warning', '密码错误')

        else:
            pass


def showLoginUI(db, cursor):
    app = QtWidgets.QApplication(sys.argv)
    loginUI = LogIn(db, cursor)
    loginUI.show()
    sys.exit(app.exec_())
