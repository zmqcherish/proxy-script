import logging
import json
import re
import os
import pickle
import requests
import random
from jsonpath import JSONPath
from time import sleep, time
from urllib.request import urlretrieve
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


@except_decorative
def get_json_file(file_path):
	with open(file_path, 'r', encoding='utf-8') as json_file:
		return json.load(json_file)

def save_json_file(file_path, save_item):
	with open(file_path, 'w', encoding='utf-8') as json_file:
		json.dump(save_item, json_file, ensure_ascii = False)


def create_folder(path):
	if os.path.exists(path):
		return
	os.mkdir(path)


def get_file_suffix(path):
	return os.path.splitext(path)[-1]


def get_pickle_file(file_path):
	with open(file_path, 'rb') as pickle_file:
		return pickle.load(pickle_file)


def save_pickle(file_path, data):
	with open(file_path, 'wb') as code_file:
		pickle.dump(data, code_file)


def get_json_val(item, path, get_first=False):
	res = JSONPath(path).parse(item)
	if res and get_first:
		return res[0]
	return res