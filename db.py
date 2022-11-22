# Created by Delitel

import sqlite3


class SQLither:

	def __init__(self, database):
		self.conn = sqlite3.connect(database)
		self.c = self.conn.cursor()

		self.c.execute("""CREATE TABLE IF NOT EXISTS files
					(file_name TEXT, size_of INTEGER)""")


	def get_files(self):
		return self.c.execute("SELECT * FROM files").fetchall()

	def get_file_info(self, file_name):
		return self.c.execute("SELECT * FROM files WHERE file_name=?", (file_name,)).fetchone()

	def exists_file(self, file_name):
		return bool(self.c.execute("SELECT * FROM files WHERE file_name=?", (file_name,)).fetchone())

	def add_files(self, file_name, size_of):
		self.c.execute("INSERT INTO files VALUES(?,?)", (file_name, size_of,))
		self.conn.commit()

	def update_files(self, file_name, size_of):
		self.c.execute("UPDATE files SET size_of=? WHERE file_name=?", (size_of, file_name,))
		self.conn.commit()

	def delete_files(self, file_name):
		self.c.execute("DELETE FROM files WHERE file_name=?", (file_name,))
		self.conn.commit()
