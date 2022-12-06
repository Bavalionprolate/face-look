import mysql.connector
from connect import ConnectToMySQL
from config import host, user, password, db

class Authorization(QtWidgets.QMainWindow):
	def __init__(self):
        
		