import logging
import json
import re
from time import sleep
from datetime import datetime, timedelta

def except_decorative(func):
	def decorator(*args, **keyargs):
		try:
			return func(*args, **keyargs)
		except Exception as e:
			logging.error(f'handle {func.__name__} error: {e}')
	return decorator


def append_txt_file(save_item, file_path='1.txt', end='\n'):
	with open(file_path, 'a', encoding='utf8') as txt_file:
		txt_file.write(save_item + end)


def get_json_file(file_path):
	with open(file_path, 'r', encoding='utf-8') as json_file:
		return json.load(json_file)