import sys, mysql.connector #mysql-connector-python==8.0.29
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView, QAbstractItemView
from PyQt5.QtCore import pyqtSlot
from datetime import datetime
from config import host, user, password, db

from assets.ui.app_ui import Ui_MainWindow

class ConnectToMySQL():
    def __init__(self):
        self.con = None
    def connect(self):
        self.con = mysql.connector.MySQLConnection(
                host = host,
                user = user,
                password = password,
                db = db,
        )

    def get_all_data_from_db(self):
        try:
            self.connect()
            cursor = self.con.cursor(dictionary=True)
            # info_user = "SELECT * FROM `User` TABLES;"
            info_user = "SELECT * FROM User JOIN Photo_user ON User.id = Photo_user.User_id"
            cursor.execute(info_user)
            result = cursor.fetchall()
            return result

        except Exception as ex:
            print("get date fail")
            print(ex)

        finally:
            if self.con:
                self.con.close()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
   

        self.appUI = Ui_MainWindow()
        self.appUI.setupUi(self)

        self.appUI.stackedWidget.setCurrentIndex(0)
        self.appUI.btn_home_2.setChecked(True)

        self.appUI.middle_sidebar_widget.hide()

        self.btn_get_date = self.appUI.btn_get_date
        self.result_table = self.appUI.tableWidget

        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.result_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.result_table.horizontalHeader().setMinimumSectionSize(0)

        self.btn_get_date.clicked.connect(self.on_btn_get_date)

    @pyqtSlot(bool)
    def on_btn_get_date(self):
        result = ConnectToMySQL().get_all_data_from_db()

        if result:
            self.result_table.setRowCount(len(result))
            print(result)

            for row, item in enumerate(result):
                column_1_item = QtWidgets.QTableWidgetItem(str(item['id']))
                column_2_item = QtWidgets.QTableWidgetItem(str(item['login']))
                column_3_item = QtWidgets.QTableWidgetItem(str(item['password']))
                column_4_item = QtWidgets.QTableWidgetItem(str(item['fio']))
                column_5_item = QtWidgets.QTableWidgetItem(str(item['pol']))
                column_6_item = QtWidgets.QTableWidgetItem(str(item['birthday']))
                column_7_item = QtWidgets.QTableWidgetItem(str(item['address']))
                column_8_item = QtWidgets.QTableWidgetItem(str(item['photo']))

                self.result_table.setItem(row, 0, column_1_item)
                self.result_table.setItem(row, 1, column_2_item)
                self.result_table.setItem(row, 2, column_3_item)
                self.result_table.setItem(row, 3, column_4_item)
                self.result_table.setItem(row, 4, column_5_item)
                self.result_table.setItem(row, 5, column_6_item)
                self.result_table.setItem(row, 6, column_7_item)
                self.result_table.setItem(row, 7, column_8_item)

        else:
            QMessageBox.information(self, 'Warning', 'No date got from database')
            return
        


    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.appUI.middle_sidebar_widget.findChildren(QPushButton) \
                    + self.appUI.full_sidebar_widget.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [4, 4]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
            
    ## functions for changing menu page
    def on_btn_home_1_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(0)
    
    def on_btn_home_2_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(0)

    def on_btn_db_1_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(1)

    def on_btn_db_2_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(1)

    def on_btn_add_1_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(2)

    def on_btn_add_2_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(2)

    def on_btn_settings_1_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(3)

    def on_btn_settings_2_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(3)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("assets/style/app_style.qss", "r") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())