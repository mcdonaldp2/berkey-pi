import sqlite3
import os
from datetime import datetime,date
import calendar
import json
from flask import Flask
import sys

def get_sqlite_connection():
	path = get_file_path() + '/berkey.db'
	
	if (not os.path.isfile(path)):
		init_sqlite_db()

	return sqlite3.connect(path)

def get_file_path():
	return os.path.dirname(os.path.realpath(__file__))

def init_sqlite_db():
	execute_sql_file(get_file_path() + '/sql/init/create-berkeyconfig-table.sql')
	execute_sql_file(get_file_path() + '/sql/init/populate-berkeymodel-table.sql')
	execute_sql_file(get_file_path() + '/sql/init/create-berkeymodel-table.sql')
	execute_sql_file(get_file_path() + '/sql/init/create-fill-table.sql')	

def execute_sql_file(filepath):
	connection = get_sqlite_connection()
	cursor = connection.cursor()

	sql_file = open(filepath)
	sql_as_string = sql_file.read()
	
	cursor.executescript(sql_as_string)
	connection.commit()
	connection.close()

def execute_selectquery_file(filepath):
	connection = get_sqlite_connection()
	cursor = connection.cursor()

	sql_file = open(filepath)
	sql_string = sql_file.read()
	cursor.execute(sql_string)
	rows = cursor.fetchall()
	connection.close()

	return rows

def get_fills_this_week():
	results = execute_selectquery_file(get_file_path() + '/sql/get/get-fills-this-week.sql')
	return results

def get_fills_last_week():
	results = execute_selectquery_file(get_file_path() + '/sql/get/get-fills-last-week.sql')
	return results

def get_total_fills():
	results = execute_selectquery_file(get_file_path() + '/sql/get/get-total-fills.sql')
	return results[0][0]

def get_ytd_fills():
	results = execute_selectquery_file(get_file_path() + '/sql/get/get-ytd-fills.sql')
	return results[0][0]

def get_day_of_the_week():
	return calendar.day_name[date.today().weekday()]

def get_berkeyconfig():
	results = execute_selectquery_file(get_file_path() + '/sql/get/get-berkeyconfig.sql')
	if (len(results) == 1):
		return BerkeyConfig(results[0][0], results[0][1], results[0][2], results[0][3], results[0][4])
	else:
		return BerkeyConfig()

def get_berkeymodels():
	results = execute_selectquery_file(get_file_path() + '/sql/get/get-berkeymodels.sql')
	models = []
	if (len(results) > 0):
		for row in results:
			models.append(BerkeyModel(row[0], row[1], row[2]))

	return models

def log_fill():
	connection = get_sqlite_connection()
	cursor = connection.cursor()
	cursor.execute(
		"Insert into BerkeyFillLog (BerkeyConfigId, FillTime, FillDayOfWeek) values((select max(FilterConfigId) from BerkeyConfig), ? , ?)", (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), get_day_of_the_week())
	)
	
	connection.commit()
	connection.close()

def upsert_berkeyconfig(form):
	response = None

	if (form['action'] == 'update'):
		response = update_berkeyconfig(form)
	elif (form['action'] == 'create'):
		response = create_berkeyconfig(form)

	return response

def create_berkeyconfig(form):
	connection = get_sqlite_connection()
	config_response = BerkeyConfigResponse(False, None)

	try:
		new_config = BerkeyConfig(
			None,
			int(form['model']), None, 
			int(form['elementcount']), 
			None
		)

		print("Creating Config!")
		cursor = connection.cursor()
		cursor.execute(
			'''Insert into BerkeyConfig 
				(ModelId, NumberOfFilterElements)
				VALUES (?, ?);
			''',
			(
				new_config.model_id,
				new_config.number_of_filter_elements,
			)
		)
		connection.commit()
		config_response = BerkeyConfigResponse(True, None)
	except Exception as e:
		print("create failed with the following error:")
		print(str(e))
		
		config_response = BerkeyConfigResponse(False, e)
	finally:
		connection.close()
	
	return config_response

def update_berkeyconfig(form):
	connection = get_sqlite_connection()
	config_response = BerkeyConfigResponse(False, None)

	try:
		existing_config = get_berkeyconfig()
		new_config = BerkeyConfig(
				int(form['filter_config_id']), 
				int(form['model']), None, 
				int(form['elementcount']), 
				None
			)

		if (existing_config.filter_config_id != None and new_config.filter_config_id != None and 
			existing_config.filter_config_id == new_config.filter_config_id):
			print("Updating Config!")
			cursor = connection.cursor()
			cursor.execute(
				'''Update BerkeyConfig 
					set ModelId = ?, 
						NumberOfFilterElements = ? 
					where FilterConfigId = ?;
				''',
				(
					new_config.model_id,
					new_config.number_of_filter_elements,
					new_config.filter_config_id
				)
			)
			connection.commit()
			config_response = BerkeyConfigResponse(True, None)
	except Exception as e:
		print("update failed with the following error:")
		print(str(e))
		
		config_response = BerkeyConfigResponse(False, e)
	finally:
		connection.close()

	return config_response



class BerkeyModel:
	def __init__(self, model_id, model_name, tank_size):
		self.model_id = model_id
		self.model_name = model_name
		self.tank_size = tank_size

class BerkeyConfig:
	def __init__(self, filter_config_id, model_id, model_name, number_of_filter_elements, created_on):
		self.filter_config_id = filter_config_id
		self.model_id = model_id
		self.model_name = model_name
		self.number_of_filter_elements = number_of_filter_elements
		self.created_on = created_on

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class BerkeyConfigResponse:
	def __init__(self, is_success, error_message):
		self.is_success = is_success
		self.error_message = error_message

		