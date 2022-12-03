import os, sys, face_recognition, mysql.connector
import base64
from config import host, user, password, db

class Test():
	def __init__(self):
		self.con = None
		
	def connect(self):
		self.con = mysql.connector.MySQLConnection(
				host = host,
				user = user, 
				password = password,
				db = db,
		)

	def RetriveBlob(self):
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

	def train_model_by_img(name):
		if not os.path.exists('assets/tmp'):
			print("[error] no serch directory")
			sys.exit()

		know_encodings = []

	def main(self):
		result = self.RetriveBlob()
		for i in range(len(result)):
			id = result[i]['User_id']

			with open(f"assets/tmp/imageToSave{id}.jpg", "wb") as fh:
				fh.write(base64.decodebytes(result[i]['photo']))



if __name__ == '__main__':
	app = Test()
	app.main()