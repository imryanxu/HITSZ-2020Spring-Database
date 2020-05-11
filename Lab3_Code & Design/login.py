# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.usernoline = QtWidgets.QLineEdit(Form)
        self.usernoline.setGeometry(QtCore.QRect(160, 40, 171, 21))
        self.usernoline.setObjectName("usernoline")
        self.pwdline = QtWidgets.QLineEdit(Form)
        self.pwdline.setGeometry(QtCore.QRect(160, 100, 171, 21))
        self.pwdline.setObjectName("pwdline")
        self.nolabel = QtWidgets.QLabel(Form)
        self.nolabel.setGeometry(QtCore.QRect(70, 40, 72, 15))
        self.nolabel.setObjectName("nolabel")
        self.pwdlabel = QtWidgets.QLabel(Form)
        self.pwdlabel.setGeometry(QtCore.QRect(70, 100, 72, 15))
        self.pwdlabel.setObjectName("pwdlabel")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 160, 321, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buyerButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.buyerButton.setObjectName("buyerButton")
        self.horizontalLayout.addWidget(self.buyerButton)
        self.sellerButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.sellerButton.setObjectName("sellerButton")
        self.horizontalLayout.addWidget(self.sellerButton)
        self.adminButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.adminButton.setObjectName("adminButton")
        self.horizontalLayout.addWidget(self.adminButton)
        self.loginpushButton = QtWidgets.QPushButton(Form)
        self.loginpushButton.setGeometry(QtCore.QRect(80, 230, 93, 28))
        self.loginpushButton.setObjectName("loginpushButton")
        self.exitpushButton = QtWidgets.QPushButton(Form)
        self.exitpushButton.setGeometry(QtCore.QRect(230, 230, 93, 28))
        self.exitpushButton.setObjectName("exitpushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.nolabel.setText(_translate("Form", "用户编号"))
        self.pwdlabel.setText(_translate("Form", "用户密码"))
        self.buyerButton.setText(_translate("Form", "买家"))
        self.sellerButton.setText(_translate("Form", "卖家"))
        self.adminButton.setText(_translate("Form", "管理员"))
        self.loginpushButton.setText(_translate("Form", "登录"))
        self.exitpushButton.setText(_translate("Form", "退出"))
