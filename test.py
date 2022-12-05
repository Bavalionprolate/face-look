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

	def main(self):
		result = self.RetriveBlob()
		for i in range(len(result)):
			id = result[i]['User_id']

			with open(f"assets/tmp/tmp{id}.jpg", "wb") as fh:
				fh.write(base64.decodebytes(result[i]['photo']))

			if not os.path.exists('assets/tmp'):
				print("[error] no serch directory")
				sys.exit()

			know_encodings = []
			images = os.listdir('assets/tmp')

			for(j, image) in enumerate(images):
				if (image == f'tmp{id}.jpg'):
					print(f"[+] processing img {j + 1}/{len(images)}")
					print(image)

					face_img = face_recognition.load_image_file(f'assets/tmp/{image}')
					face_enc = face_recognition.face_encodings(face_img)[0]

					if len(know_encodings) == 0:
						know_encodings.append(face_enc)
					else:
						for item in range(0, len(know_encodings)):
							result = face_recognition.compare_faces([face_enc], know_encodings[item])
							print(result)

							if result[0]:
								know_encodings.append(face_enc)
								print("Тот же человек")
								break
							else:
								print("Кто-то другой")
								break
				# print(know_encodings)
			print(f'Длинна {len(know_encodings)}')


if __name__ == '__main__':
	app = Test()
	app.main()