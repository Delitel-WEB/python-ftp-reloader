# Created by Delitel

import os
import subprocess
import sys
import cfg
from log import LOGGER
from db import SQLither
import time

os.chdir(cfg.daemon_dir)


db = SQLither("db.db")
log = LOGGER("daemon_log")
log.info("Демон запущен!")
main_file = os.path.join(cfg.working_dir, cfg.app_name)

os.chdir(cfg.working_dir)


process = None



if db.exists_file(main_file):
	log.info(f"Запускаем процесс: {main_file}")
	process = subprocess.Popen([sys.executable, main_file])
while True:
	time.sleep(3)
	updated = False
	files = os.walk(cfg.working_dir)

	for adress, dirs, files_ in files:
		for file in files_:

			all_path = os.path.join(adress, file)
			filename, file_extension = os.path.splitext(all_path)

			if file_extension in cfg.extensions:
				size_of = os.path.getsize(all_path)

				if not db.exists_file(all_path):
					log.info(f"Добавлен файл: {all_path}")
					db.add_files(all_path, size_of)
					updated = True
				else:
					file_info = db.get_file_info(all_path)

					if file_info[1] != size_of:
						log.info(f"Файл обновлён: {all_path}")
						db.update_files(all_path, size_of)
						updated = True

	database_files = db.get_files()
	for file in database_files:
		if not os.path.exists(file[0]):
			log.info(f"Файл удалён: {file[0]}")
			db.delete_files(file[0])
			updated = True


	if updated:
		if process:
			process.kill()
			log.info("Процесс убит!")
		
		log.info(f"Запускаем процесс: {main_file}")
		process = subprocess.Popen([sys.executable, main_file])

