import sys, mysql.connector #mysql-connector-python==8.0.29
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView, QAbstractItemView
from PyQt5.QtCore import pyqtSlot, QObject, QEvent, Qt
from PyQt5.QtGui import QPixmap
from datetime import datetime
from config import host, user, password, db

import base64
from PIL import Image #pip install Pillow

from assets.ui.ui_app import Ui_MainWindow

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
			info_user = "SELECT * FROM User"
			cursor.execute(info_user)
			result = cursor.fetchall()
			return result

		except Exception as ex:
			print("get date fail")
			print(ex)

		finally:
			if self.con:
				self.con.close()

	def RetriveBlob(self, ID):
		try:
			self.connect()
			cursor = self.con.cursor(dictionary=True)
			sql = f"SELECT photo FROM `photo_user` WHERE `User_id` = '{ID}'"
			cursor.execute(sql)
			result = cursor.fetchone()

			return result
		except Exception as ex:
			print("get date fail")
			print(ex)

		finally:
			if self.con:
				self.con.close()

	def UploadData(self, lineEdit_id, lineEdit_login, lineEdit_password, lineEdit_fio, lineEdit_pol, lineEdit_data, lineEdit_addres):
		try:
			self.connect()
			cursor = self.con.cursor(dictionary=True)
			sql = f"INSERT INTO User (`id`, `login`, `password`, `fio`, `pol`, `birthday`, `address`) VALUES ('{lineEdit_id}', '{lineEdit_login}', '{lineEdit_password}', '{lineEdit_fio}', '{lineEdit_pol}', '{lineEdit_data}', '{lineEdit_addres}')"
			cursor.execute(sql)
			result = cursor.fetchone()
			self.con.commit()

			return result
		except Exception as ex:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText(f"{ex}")
			msgBox.setWindowTitle("Ошибка")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()


		finally:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText("Новый пользователь добавлен")
			msgBox.setWindowTitle("Уведомление")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()
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
		self.btn_add_user_in_bd = self.appUI.btn_add_user_in_bd
		
		self.result_table = self.appUI.tableWidget

		self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		self.result_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.result_table.horizontalHeader().setMinimumSectionSize(0)
		self.result_table.viewport().installEventFilter(self)

		self.btn_get_date.clicked.connect(self.on_btn_get_date)
		self.btn_add_user_in_bd.clicked.connect(self.on_btn_add_user_in_bd)

	def getsamerowcell(self, columnname):

		row = self.result_table.currentItem().row()
		# col = widget.currentItem().column()

		# loop through headers and find column number for given column name
		headercount = self.result_table.columnCount()
		for x in range(headercount):
			headertext = self.result_table.horizontalHeaderItem(x).text()
			if columnname == headertext:
				cell = self.result_table.item(row, x).text()  # get cell at row, col
				return cell
		
		
	def eventFilter(self, source, event):
		if self.result_table.selectedIndexes() != []:
			
			if event.type() == QEvent.MouseButtonRelease:
				if event.button() == Qt.LeftButton:
					
					col = self.result_table.currentColumn()

					if (col == 7):
						try:
							db = ConnectToMySQL()
							image = db.RetriveBlob(self.getsamerowcell('Идентификатор'))
							for i in image:
													
								with open("assets/tmp/imageToSave.jpg", "wb") as fh:
									fh.write(base64.decodebytes(image[i] ))

							im = Image.open('assets/tmp/imageToSave.jpg')
							im.show()
						except:
							msgBox = QMessageBox()
							msgBox.setIcon(QMessageBox.Information)
							msgBox.setText("У данного пользователся нет фото в базе данных")
							msgBox.setWindowTitle("Ошибка")
							msgBox.setStandardButtons(QMessageBox.Ok)
							msgBox.exec()
 
		return QObject.event(source, event)

	@pyqtSlot(bool)
	def on_btn_add_user_in_bd(self):
		lineEdit_login = self.appUI.lineEdit_login.text()
		lineEdit_id = self.appUI.lineEdit_id.text()
		lineEdit_password = self.appUI.lineEdit_password.text()
		lineEdit_fio = self.appUI.lineEdit_fio.text()
		lineEdit_pol = self.appUI.lineEdit_pol.text()
		lineEdit_data = self.appUI.lineEdit_data.text()
		lineEdit_addres = self.appUI.lineEdit_addres.text()
		db = ConnectToMySQL()
		db.UploadData(lineEdit_id, lineEdit_login, lineEdit_password, lineEdit_fio, lineEdit_pol, lineEdit_data, lineEdit_addres)
		


	@pyqtSlot(bool)
	def on_btn_get_date(self):
		result = ConnectToMySQL().get_all_data_from_db()

		if result:
			self.result_table.setRowCount(len(result))

			for row, item in enumerate(result):
				column_1_item = QtWidgets.QTableWidgetItem(str(item['id']))
				column_2_item = QtWidgets.QTableWidgetItem(str(item['login']))
				column_3_item = QtWidgets.QTableWidgetItem(str(item['password']))
				column_4_item = QtWidgets.QTableWidgetItem(str(item['fio']))
				column_5_item = QtWidgets.QTableWidgetItem(str(item['pol']))
				column_6_item = QtWidgets.QTableWidgetItem(str(item['birthday']))
				column_7_item = QtWidgets.QTableWidgetItem(str(item['address']))
				column_8_item = QtWidgets.QTableWidgetItem(str('view'))			

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