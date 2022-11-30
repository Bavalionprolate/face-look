import sys, mysql.connector #mysql-connector-python==8.0.29
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView, QAbstractItemView, QDialog, QFileDialog
from PyQt5.QtCore import pyqtSlot, QObject, QEvent, Qt, QSortFilterProxyModel
from PyQt5.QtCore import pyqtSlot, QObject, QEvent, Qt
from PyQt5.QtGui import QPixmap
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

	def get_id_data_from_db(self):
		try:
			self.connect()
			cursor = self.con.cursor()
			info_user = "SELECT id FROM user"
			cursor.execute(info_user)
			result = cursor.fetchall()
			return result

		except Exception as ex:
			print("get date fail")
			print(ex)

		finally:
			if self.con:
				self.con.close()

	def get_all_data_from_db(self):
		try:
			self.connect()
			cursor = self.con.cursor(dictionary=True)
			info_user = "SELECT * FROM user"
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

	def UploadData(self, lineEdit_id, lineEdit_login, lineEdit_password, lineEdit_fio, lineEdit_pol, lineEdit_data, lineEdit_addres, label_status):
		try:
			self.connect()
			cursor = self.con.cursor()
			sql = f"INSERT INTO user (`id`, `login`, `password`, `fio`, `pol`, `birthday`, `address`) VALUES ('{lineEdit_id}', '{lineEdit_login}', '{lineEdit_password}', '{lineEdit_fio}', '{lineEdit_pol}', '{lineEdit_data}', '{lineEdit_addres}');"
			cursor.execute(sql)
			self.con.commit()
			

			with open(label_status, 'rb') as f:
				photo = f.read()
			encodestring = base64.b64encode(photo)
			
			sql = f"INSERT INTO photo_user (User_id, photo) values ({lineEdit_id}, %s)"
			cursor.execute(sql, (encodestring, ))
			self.con.commit()
				
		except Exception as ex:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText(f"{ex}")
			msgBox.setWindowTitle("Ошибка")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()

			self.con.rollback() 

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

		self.btn_get_date_1 = self.appUI.btn_get_date_1
		self.btn_get_date_2 = self.appUI.btn_get_date_2
		self.btn_add_user_in_bd = self.appUI.btn_add_user_in_bd
		self.btn_upload_user_photo = self.appUI.btn_upload_user_photo
		self.btn_clear_table_1 = self.appUI.btn_clear_table_1
		self.btn_clear_table_2 = self.appUI.btn_clear_table_2
		self.btn_add_upload = self.appUI.btn_add_upload
		
		self.result_table_1 = self.appUI.tableWidget
		self.result_table_2 = self.appUI.tableWidget_2

		self.result_table_2.hide()
		self.appUI.widget_10.hide()

		self.result_table_1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		self.result_table_1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.result_table_1.horizontalHeader().setMinimumSectionSize(0)
		self.result_table_1.viewport().installEventFilter(self)

		self.result_table_1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		self.result_table_1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.result_table_1.horizontalHeader().setMinimumSectionSize(0)
		self.result_table_1.viewport().installEventFilter(self)

		self.result_table_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

		self.btn_get_date_1.clicked.connect(self.on_btn_get_date_1)
		self.btn_get_date_2.clicked.connect(self.on_btn_get_date_2)
		self.btn_add_user_in_bd.clicked.connect(self.on_btn_add_user_in_bd)
		self.btn_upload_user_photo.clicked.connect(self.on_btn_upload_user_photo)
		self.btn_clear_table_1.clicked.connect(self.on_btn_clear_table_1)
		self.btn_clear_table_2.clicked.connect(self.on_btn_clear_table_2)

		# self.btn_add_upload.clicked.connect(self.on_btn_add_upload)

	def getsamerowcell(self, columnname, table):

		row = table.currentItem().row()

		headercount = table.columnCount()
		for x in range(headercount):
			headertext = table.horizontalHeaderItem(x).text()
			if columnname == headertext:
				cell = table.item(row, x).text()

		row = self.result_table_1.currentItem().row()
		# col = widget.currentItem().column()

		# loop through headers and find column number for given column name
		headercount = self.result_table_1.columnCount()
		for x in range(headercount):
			headertext = self.result_table_1.horizontalHeaderItem(x).text()
			if columnname == headertext:
				cell = self.result_table_1.item(row, x).text()  # get cell at row, col
				return cell
		
	def eventFilter(self, source, event):
		if self.result_table_1.selectedIndexes() != []:
			
			if event.type() == QEvent.MouseButtonRelease:
				if event.button() == Qt.LeftButton:
					
					col = self.result_table_1.currentColumn()

					if (col == 6):
						try:
							db = ConnectToMySQL()
							image = db.RetriveBlob(self.getsamerowcell('Идентификатор', self.result_table_1))
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

	# @pyqtSlot(bool)
	# def on_btn_add_upload(self):
	# 		print(col = self.result_table_2.currentColumn())		

	@pyqtSlot(bool)
	def on_btn_clear_table_1(self):
		while (self.result_table_1.rowCount() > 0):
			self.result_table_1.removeRow(0)

	@pyqtSlot(bool)
	def on_btn_clear_table_2(self):
		while (self.result_table_2.rowCount() > 0):
			self.result_table_2.removeRow(0)
	
	@pyqtSlot(bool)
	def on_btn_upload_user_photo(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file', "")
		self.appUI.label_status.setText(fname[0])

	@pyqtSlot(bool)
	def on_btn_clear_table_1(self):
		while (self.result_table_1.rowCount() > 0):
			self.result_table_1.removeRow(0)

	@pyqtSlot(bool)
	def on_btn_clear_table_2(self):
		while (self.result_table_2.rowCount() > 0):
			self.result_table_2.removeRow(0)
	
	@pyqtSlot(bool)
	def on_btn_upload_user_photo(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file', "")
		self.appUI.label_status.setText(fname[0])

	@pyqtSlot(bool)
	def on_btn_add_user_in_bd(self):
		lineEdit_login = self.appUI.lineEdit_login.text()
		lineEdit_id = self.appUI.lineEdit_id.text()
		lineEdit_password = self.appUI.lineEdit_password.text()
		lineEdit_fio = self.appUI.lineEdit_fio.text()
		lineEdit_pol = self.appUI.lineEdit_pol.text()
		lineEdit_data = self.appUI.lineEdit_data.text()
		lineEdit_addres = self.appUI.lineEdit_addres.text()
		label_status = self.appUI.label_status.text()
		if (label_status == ''):
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText("Вы не добавили фото!\nДобавьте обязательно фотографию")
			msgBox.setWindowTitle("Ошибка")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()
		elif (lineEdit_id == "" or lineEdit_password == "" or lineEdit_fio == "" or lineEdit_pol  == "" or lineEdit_data == "" or lineEdit_addres == ""):
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText("Вы не заполнили все строки данными")
			msgBox.setWindowTitle("Ошибка")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()
		else:
			db = ConnectToMySQL()
			db.UploadData(lineEdit_id, lineEdit_login, lineEdit_password, lineEdit_fio, lineEdit_pol, lineEdit_data, lineEdit_addres, label_status)

	@pyqtSlot(bool)
	def on_btn_get_date_1(self):
		result = ConnectToMySQL().get_all_data_from_db()

		if result:
			self.result_table_1.setRowCount(len(result))

			for row, item in enumerate(result):
				column_1_item = QtWidgets.QTableWidgetItem(str(item['id']))
				column_2_item = QtWidgets.QTableWidgetItem(str(item['login']))
				column_3_item = QtWidgets.QTableWidgetItem(str(item['fio']))
				column_4_item = QtWidgets.QTableWidgetItem(str(item['pol']))
				column_5_item = QtWidgets.QTableWidgetItem(str(item['birthday']))
				column_6_item = QtWidgets.QTableWidgetItem(str(item['address']))
				column_7_item = QtWidgets.QTableWidgetItem(str('view'))			

				self.result_table_1.setItem(row, 0, column_1_item)
				self.result_table_1.setItem(row, 1, column_2_item)
				self.result_table_1.setItem(row, 2, column_3_item)
				self.result_table_1.setItem(row, 3, column_4_item)
				self.result_table_1.setItem(row, 4, column_5_item)
				self.result_table_1.setItem(row, 5, column_6_item)
				self.result_table_1.setItem(row, 6, column_7_item)

	@pyqtSlot(bool)
	def on_btn_get_date_2(self):
		result = ConnectToMySQL().get_all_data_from_db()

		if result:
			self.result_table_2.setRowCount(len(result))

			for row, item in enumerate(result):
				column_1_item = QtWidgets.QTableWidgetItem(str(item['id']))
				column_2_item = QtWidgets.QTableWidgetItem(str(item['login']))
				column_3_item = QtWidgets.QTableWidgetItem(str(item['password']))
				column_4_item = QtWidgets.QTableWidgetItem(str(item['fio']))
				column_5_item = QtWidgets.QTableWidgetItem(str(item['pol']))
				column_6_item = QtWidgets.QTableWidgetItem(str(item['birthday']))
				column_7_item = QtWidgets.QTableWidgetItem(str(item['address']))	

				self.result_table_2.setItem(row, 0, column_1_item)
				self.result_table_2.setItem(row, 1, column_2_item)
				self.result_table_2.setItem(row, 2, column_3_item)
				self.result_table_2.setItem(row, 3, column_4_item)
				self.result_table_2.setItem(row, 4, column_5_item)
				self.result_table_2.setItem(row, 5, column_6_item)
				self.result_table_2.setItem(row, 6, column_7_item)

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