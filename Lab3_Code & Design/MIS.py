from func_signin import showLoginUI
import pymysql
import sys
from PyQt5 import QtWidgets


db = pymysql.connect(host="localhost", user="root", password="HelloSQL", database="mis")
cursor = db.cursor()

showLoginUI(db, cursor)