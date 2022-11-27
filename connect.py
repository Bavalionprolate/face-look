import mysql.connector, sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QApplication
import base64
import io
import PIL.Image
# from assets.ui.connector_ui import Ui_Form
from config import host, user, password, db

# from app import MainWindow

# class Form(QWidget):
# 	def __init__(self):
# 		super(Form, self).__init__()

# 		# self.appUI = Ui_Form()
# 		# self.appUI.setupUi(self)

# 		self.mysqlconnect()

def mysqlconnect():

	with open('Аннотация 2022-11-27 225441.jpg', 'rb') as f:
		photo = f.read()
	encodestring = base64.b64encode(photo)
		
	# To connect MySQL database
	con = mysql.connector.MySQLConnection(
		host = host,
		user = user, 
		password = password,
		db = db,
		)
		
	cur = con.cursor()
	sql = f"INSERT INTO photo_user (User_id, photo) values (2, %s)"
	cur.execute(sql, (encodestring, ))
	con.commit()
		
		# To close the connection
	con.close()

# if __name__ == '__main__':
# 	app = QApplication(sys.argv)

# 	# with open("assets/style/app_style.qss", "r") as style_file:
# 	#     style_str = style_file.read()

# 	# app.setStyleSheet(style_str)


# 	window = Form()
# 	window.show()
# 	sys.exit(app.exec())
  

# import pymysql
  
# def mysqlconnect():
#     # To connect MySQL database
#     conn = pymysql.connect(
#         host='web.edu',
#         user='19261', 
#         password = "vqgyhz",
#         db='19261_face_look',
#         )
	  
#     cur = conn.cursor()
#     cur.execute("INSERT INTO User (`id`, `login`, `password`, `fio`, `pol`, `birthday`, `address`) VALUES (1, 'bavalion', 34781, 'Громыко Иван Александрович', 'Мужской', '2003-03-27', 'г.Иркутск, р.п. Маркова')")
#     conn.commit()
	  
#     # To close the connection
#     conn.close()
  
# # Driver Code
if __name__ == "__main__" :
    mysqlconnect()