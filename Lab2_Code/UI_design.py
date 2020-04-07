import sys
from lab2demo import *
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class lab2demo(Ui_MainWindow):

    # 设置各种点击反应
    def setupResponse(self):
        self.setResultTable()
        self.connectButton.clicked.connect(self.connectDatabase)
        self.closeButton.clicked.connect(self.closeDatabase)

        self.clearButton.clicked.connect(self.clear_all)
        self.selectButton.clicked.connect(self.func_select)
        self.insertButton.clicked.connect(self.func_insert)
        self.deleteButton.clicked.connect(self.func_delete)
        self.updateButton.clicked.connect(self.func_update)

    # 初始化表格
    def setResultTable(self):
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["姓名", "编号", "住址", "工资", "直接领导编号", "所属部门编号"])

        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 50)
        self.tableWidget.setColumnWidth(2, 250)
        self.tableWidget.setColumnWidth(3, 75)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 100)

    # 将获取到的data写入表格中
    def dataToTableWidget(self, data):
        self.tableWidget.setRowCount(len(data))
        for i in range(0, len(data)):
            for j in range(0, 6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data[i][j])))

    # 连接并初始化数据库内容
    def connectDatabase(self):
        try:
            self.__conn = pymysql.connect(host="localhost", user="root", password="HelloSQL", database="company")
            self.statusbar.showMessage("Connected")
            self.__sql = "select * from employee"
            self.__cursor = self.__conn.cursor()
            self.sqltextBrowser.setText(self.__sql)
            try:
                self.__cursor.execute(self.__sql)
                data = self.__cursor.fetchall()
                self.dataToTableWidget(data)
            except:
                self.statusbar.showMessage("Fail to initialize")
        except:
            self.statusbar.showMessage("Error in connecting to MySQL")
        self.__cursor.close()

    # 断开数据库
    def closeDatabase(self):
        try:
            self.__conn.close()
            self.statusbar.showMessage("Database closed!")
        except:
            self.statusbar.showMessage("Error in closing MySQL")

    # 清除填写的表单数据
    def clear_all(self):
        self.enamecheckBox.setCheckState(False)
        self.essncheckBox.setCheckState(False)
        self.addresscheckBox.setCheckState(False)
        self.salarycheckBox.setCheckState(False)
        self.superssncheckBox.setCheckState(False)
        self.dnocheckBox.setCheckState(False)
        self.enamelineEdit.clear()
        self.essnlineEdit.clear()
        self.addresslineEdit.clear()
        self.salarylineEdit.clear()
        self.superssnlineEdit.clear()
        self.dnolineEdit.clear()

    # 选择
    def func_select(self):
        more = 0
        self.__sql = "select * from employee where"

        if self.enamecheckBox.isChecked():
            more = 1
            self.__sql += " ename = \'" + self.enamelineEdit.text() + "\'"

        if self.essncheckBox.isChecked():
            if more != 0:
                self.__sql += " and "
            more = 1
            self.__sql += " essn = \'" + self.essnlineEdit.text() + "\'"

        if self.addresscheckBox.isChecked():
            if more != 0:
                self.__sql += " and "
            more = 1
            self.__sql += " address like \'%" + self.addresslineEdit.text() + "%\'"

        if self.salarycheckBox.isChecked():
            if more != 0:
                self.__sql += " and "
            more = 1
            self.__sql += " salary = " + self.salarylineEdit.text()

        if self.superssncheckBox.isChecked():
            if more != 0:
                self.__sql += " and "
            more = 1
            self.__sql += " superssn = \'" + self.superssnlineEdit.text() + "\'"

        if self.dnocheckBox.isChecked():
            if more != 0:
                self.__sql += " and "
            self.__sql += " dno = \'" + self.dnolineEdit.text() + "\'"

        self.sqltextBrowser.setText(self.__sql)
        self.__cursor = self.__conn.cursor()
        try:
            self.__cursor.execute(self.__sql)
            data = self.__cursor.fetchall()
            self.dataToTableWidget(data)
            self.statusbar.showMessage("Select %d employees successfully." % len(data))
        except:
            self.statusbar.showMessage("Fail to fetch data!")
        self.__cursor.close()
        return

    # 插入（只支持添加所有属性）
    def func_insert(self):
        self.enamecheckBox.setCheckState(True)
        self.essncheckBox.setCheckState(True)
        self.addresscheckBox.setCheckState(True)
        self.salarycheckBox.setCheckState(True)
        self.superssncheckBox.setCheckState(True)
        self.dnocheckBox.setCheckState(True)
        self.__sql = "insert into employee values (\'" + self.enamelineEdit.text() + "\',\'" \
                     + self.essnlineEdit.text() + "\',\'" + self.addresslineEdit.text() + "\'," \
                     + self.salarylineEdit.text() + ",\'" + self.superssnlineEdit.text() + "\',\'" \
                     + self.dnolineEdit.text() + "\')"
        self.sqltextBrowser.setText(self.__sql)
        self.__cursor = self.__conn.cursor()
        try:
            self.__cursor.execute(self.__sql)
            data = self.__cursor.fetchall()
            self.__conn.commit()
            self.dataToTableWidget(data)
        except:
            self.statusbar.showMessage("Fail to insert data!")
        self.statusbar.showMessage("Insert successfully.")
        self.__cursor.close()
        return

    # 删除（只支持通过essn来删除）
    def func_delete(self):
        self.enamecheckBox.setCheckState(False)
        self.essncheckBox.setCheckState(True)
        self.addresscheckBox.setCheckState(False)
        self.salarycheckBox.setCheckState(False)
        self.superssncheckBox.setCheckState(False)
        self.dnocheckBox.setCheckState(False)
        self.__sql = "delete from employee where essn = \'" + self.essnlineEdit.text() + "\'"
        self.sqltextBrowser.setText(self.__sql)
        self.__cursor = self.__conn.cursor()
        try:
            self.__cursor.execute(self.__sql)
            data = self.__cursor.fetchall()
            self.__conn.commit()
            self.dataToTableWidget(data)
        except:
            self.statusbar.showMessage("Fail to delete data!")
        self.statusbar.showMessage("Delete successfully.")
        self.__cursor.close()
        return

    # 更新
    def func_update(self):
        more = 0
        self.__sql = "update employee set "

        if self.enamecheckBox.isChecked():
            more = 1
            self.__sql += " ename = \'" + self.enamelineEdit.text() + "\'"

        if self.addresscheckBox.isChecked():
            if more != 0:
                self.__sql += " , "
            more = 1
            self.__sql += " address = \'" + self.addresslineEdit.text() + "\'"

        if self.salarycheckBox.isChecked():
            if more != 0:
                self.__sql += " , "
            more = 1
            self.__sql += " salary = " + self.salarylineEdit.text()

        if self.superssncheckBox.isChecked():
            if more != 0:
                self.__sql += " , "
            more = 1
            self.__sql += " superssn = \'" + self.superssnlineEdit.text() + "\'"

        if self.dnocheckBox.isChecked():
            if more != 0:
                self.__sql += " , "
            self.__sql += " dno = \'" + self.dnolineEdit.text() + "\'"

        self.essncheckBox.setCheckState(True)
        self.__sql += " where essn = \'" + self.essnlineEdit.text() + "\'"

        self.sqltextBrowser.setText(self.__sql)
        self.__cursor = self.__conn.cursor()
        try:
            self.__cursor.execute(self.__sql)
            self.__conn.commit()
            data = self.__cursor.fetchall()
            self.dataToTableWidget(data)
        except:
            self.statusbar.showMessage("Fail to update data!")
        self.statusbar.showMessage("Update successfully.")
        self.__cursor.close()
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = lab2demo()
    ui.setupUi(MainWindow)
    ui.setupResponse()
    MainWindow.show()
    sys.exit(app.exec_())
