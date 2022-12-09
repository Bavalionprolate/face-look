import sys, os, base64, face_recognition, datetime, shutil, re
import mysql.connector, base64
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView, QAbstractItemView, QDialog, QFileDialog
from PyQt5.QtCore import pyqtSlot, QObject, QEvent, Qt, QSortFilterProxyModel
from PyQt5.QtCore import pyqtSlot, QObject, QEvent, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image #pip install Pillow

from assets.ui.ui_app import Ui_MainWindow
from assets.ui.ui_authorization import Ui_Authorization

from config import host, user, password, db

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

	def rules(self):
		try:
			self.connect()
			cursor = self.con.cursor(dictionary=True)
			info_user = "SELECT * FROM prava"
			cursor.execute(info_user)
			result = cursor.fetchall()
			return result

		except Exception as ex:
			print("get date fail")
			print(ex)

		finally:
			if self.con:
				self.con.close()	

	def connect_auth_user(self):
		try:
			self.connect()
			cursor = self.con.cursor(dictionary=True)
			info_user = "SELECT id, login, password FROM user"
			cursor.execute(info_user)
			result = cursor.fetchall()
			return result

		except Exception as ex:
			print("get date fail")
			print(ex)

		finally:
			if self.con:
				self.con.close()	

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

	def RetrieveOutBlob(self, id):
		try:
			self.connect()
			cursor = self.con.cursor(dictionary=True)
			sql = f"SELECT * FROM `user` WHERE user.id = {id}"
			cursor.execute(sql)
			result = cursor.fetchone()
			return result

		except Exception as ex:
			print("get date fail")
			print(ex)

		finally:
			if self.con:
				self.con.close()

	def RetriveBlobImg(self):
		try:
			self.connect()
			cursor = self.con.cursor(dictionary=True)
			sql = f"SELECT * FROM photo_user"
			cursor.execute(sql)
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

class Authorization(QtWidgets.QWidget):
	def __init__(self):
		super(Authorization, self).__init__() 

		self.appUI = Ui_Authorization()
		self.appUI.setupUi(self)

		self.auth_user = self.appUI.pushButton
		self.status = self.appUI.label_4

		self.auth_user.clicked.connect(self.on_auth_user)

	@pyqtSlot(bool)
	def on_auth_user(self):

		self.user_login = self.appUI.lineEdit_login_auth.text()
		self.user_password = self.appUI.lineEdit_pass_auth.text()

		self.connect = ConnectToMySQL()
		result = self.connect.connect_auth_user()
		rules = self.connect.rules()
		
		for item in result:
			if (not self.user_login) or (not self.user_password):
				self.status.setText('Вы не ввели логин или пароль')
			else:
				for i in rules:
					if (str(self.user_login) == str(item['login']) and str(self.user_password) == str(item['password']) and (item['id'] == i['User_id'] and i['is_programm_user'] == 1)):
						self.status.clear()
						
						self.username = item['login']
						
						self.window = MainWindow()
						window.label_user.setText(self.username)
						
						
						if (item['id'] == i['User_id'] and i['is_admin'] == 1):
							window.btn_add_1.show()
							window.btn_add_2.show()
						else:
							window.btn_add_1.hide()
							window.btn_add_2.hide()
					
						self.close()
					elif (str(self.user_login) != str(item['login']) and str(self.user_password) == str(item['password']) or str(self.user_login) == str(item['login']) and str(self.user_password) != str(item['password'])):
						self.status.setText('Вы ввели не верный логин или пароль')
						window.label_user.clear()

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
		self.btn_add_photo = self.appUI.btn_add_photo
		self.bnt_start_process = self.appUI.pushButton_5
		self.btn_connect = self.appUI.btn_connect
		self.btn_del_connect = self.appUI.btn_del_connect
		self.btn_user = self.appUI.btn_user

		self.comboBox = self.appUI.comboBox
		self.comboBox.hide()
		
		self.btn_add_1 = self.appUI.btn_add_1
		self.btn_add_2 = self.appUI.btn_add_2
		self.btn_add_1.hide()
		self.btn_add_2.hide()

		self.label_user = self.appUI.label_user
		
		self.result_table_1 = self.appUI.tableWidget
		self.result_table_2 = self.appUI.tableWidget_2

		self.appUI.status_label_2.hide()

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

		self.btn_connect.clicked.connect(self.include_date_base)
		self.btn_del_connect.clicked.connect(self.on_btn_del_connect)
		self.btn_get_date_1.clicked.connect(self.on_btn_get_date_1)
		self.btn_get_date_2.clicked.connect(self.on_btn_get_date_2)
		self.btn_add_user_in_bd.clicked.connect(self.on_btn_add_user_in_bd)
		self.btn_upload_user_photo.clicked.connect(self.on_btn_upload_user_photo)
		self.btn_clear_table_1.clicked.connect(self.on_btn_clear_table_1)
		self.btn_clear_table_2.clicked.connect(self.on_btn_clear_table_2)
		self.btn_add_photo.clicked.connect(self.on_btn_add_photo)
		self.bnt_start_process.clicked.connect(self.on_bnt_start_process)	
		self.btn_user.clicked.connect(self.on_btn_user)

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
				cell = self.result_table_1.item(row, x).text()
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
	
	def OpenFileDiolog(self):

		fname = QFileDialog.getOpenFileName(self, 'Open file', "")
		return fname[0]
	
	@pyqtSlot(bool)
	def on_btn_user(self):
		self.window = Authorization()
		self.window.show()
		
	@pyqtSlot(bool)
	def on_bnt_start_process(self):	

		result = ConnectToMySQL().RetriveBlobImg()
		find = False

		self.appUI.label_11.setText("Идет распознавание")

		try:

			for i in range(len(result)):
				id = result[i]['User_id']

				with open(f"assets/tmp/recognition/tmp{id}.jpg", "wb") as fh:
					fh.write(base64.decodebytes(result[i]['photo']))

				if not os.path.exists('assets/tmp/recognition'):
					print("[error] no serch directory")
					sys.exit()

			know_encodings = []
			images = os.listdir('assets/tmp/recognition')
		
			for (j, image) in enumerate(images):

				face_img = face_recognition.load_image_file(f'assets/tmp/recognition/{image}')
				face_enc = face_recognition.face_encodings(face_img)[0]

				if len(know_encodings) == 0:
					know_encodings.append(face_enc)
				else:
					for item in range(0, len(know_encodings)):
						result = face_recognition.compare_faces([face_enc], know_encodings[item])

						if result[0]:
							know_encodings.append(face_enc)

							id = re.sub("[t|m|p|.|j|p|g]", "", image)

							db = ConnectToMySQL()
							info = db.RetrieveOutBlob(id)

							age = str(info['birthday']).split('-')[0]
							age = int(age) - int(datetime.datetime.now().year)
							age = re.sub("-", "", str(age))

							self.appUI.label_11.setText('Присутствует в базе данны')
							self.appUI.label_13.setText(info['fio'])
							self.appUI.label_15.setText(info['pol'])
							self.appUI.label_17.setText(str(info['birthday']))
							self.appUI.label_19.setText(age)
							self.appUI.label_21.setText(str(info['address']))

							find = True
							break
						else:
							self.appUI.label_11.setText('Такого человека нет в базе данных')
							self.appUI.label_13.clear()
							self.appUI.label_15.clear()
							self.appUI.label_17.clear()
							self.appUI.label_19.clear()
							self.appUI.label_21.clear()
			
							break
				if find:
					break 
		except Exception:
			self.appUI.label_11.setText("Лицо было не найденно")
			self.appUI.label_13.clear()
			self.appUI.label_15.clear()
			self.appUI.label_17.clear()
			self.appUI.label_19.clear()
			self.appUI.label_21.clear()

		finally:
			for image in images:
				print('удаленно фото', image)
				os.remove(f'assets/tmp/recognition/{image}')
	@pyqtSlot(bool)
	def on_btn_del_connect(self):
		date = [
			"host = ''\n",
			"user = ''\n",
			"password = ''\n",
			"db = ''\n"
		]
		with open('config.py', 'w+') as f:
			f.writelines(date)
			f.close()
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText("Подключение к база данных успешно отключено\nПерезагрузите программу для дальнейшей работы !")
		msgBox.setWindowTitle("Уведомление")
		msgBox.setStandardButtons(QMessageBox.Ok)
		msgBox.exec()
	
	@pyqtSlot(bool)
	def include_date_base(self):
		host_bd = self.appUI.lineEdit_host.text()
		user_bd = self.appUI.lineEdit_user.text()
		password_bd = self.appUI.lineEdit_password_2.text()
		name_bd = self.appUI.lineEdit_name_bd.text()
		date = [
			f"host = '{host_bd}'\n",
			f"user = '{user_bd}'\n",
			f"password = '{password_bd}'\n",
			f"db = '{name_bd}'\n"
		]

		with open('config.py', 'w+') as f:
			f.writelines(date)
			f.close()
		
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText("База данных была добавлена\nПерезагрузите программу для дальнейшей работы !")
		msgBox.setWindowTitle("Уведомление")
		msgBox.setStandardButtons(QMessageBox.Ok)
		msgBox.exec()

	@pyqtSlot(bool)
	def on_btn_add_photo(self):
		try:
			label = self.appUI.label_upload_photo
			photo = self.OpenFileDiolog()
			self.appUI.status_label_2.setText(photo)
			self.path = self.appUI.status_label_2.text()
			shutil.copyfile(self.path, "assets/tmp/recognition/past_user_image.jpg")
			label.setPixmap(QPixmap(photo).scaled(500, 690))
			label.setScaledContents(True)
		except Exception:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText("Вы не вставили фото")
			msgBox.setWindowTitle("Ошибка")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()

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
		self.appUI.label_status.setText(self.OpenFileDiolog())

	@pyqtSlot(bool)
	def on_btn_clear_table_1(self):
		while (self.result_table_1.rowCount() > 0):
			self.result_table_1.removeRow(0)

	@pyqtSlot(bool)
	def on_btn_clear_table_2(self):
		while (self.result_table_2.rowCount() > 0):
			self.result_table_2.removeRow(0)

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