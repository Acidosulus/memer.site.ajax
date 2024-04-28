from bson import json_util,ObjectId
from pymongo import MongoClient
from datetime import datetime, timedelta
from rich import print
import json

class MessageManager:
	def __init__(self, db_url, db_name, collection_name):
		self.client = MongoClient(db_url)
		self.db = self.client[db_name]
		self.collection = self.db[collection_name]
	
	@staticmethod
	def prepare_result(presult):
		result = list(presult)
		for element in result:
			if '_id' in element:
				element['_id']		=	str(element['_id'])
				element['id']		=	element['_id']
		return result


	def save_message(self, username, icon_name, message_text, hyperlink, date=datetime.now()):
		message = {
			"username": username,
			"dt": date,
			"icon": icon_name,
			"message": message_text,
			"hyperlink": hyperlink
		}
		self.collection.insert_one(message)

	def get_last_messages(self, username, num_messages):
		messages = self.collection.find({"username": username}).sort("dt", -1).limit(num_messages)
		return self.prepare_result(messages)

	def get_messages_since_id(self, username, message_id):
		print(f'get_messages_since_id(self, "{username}", "{message_id}"):')
		messages = self.collection.find({"username": username, "_id": {"$gt": ObjectId(message_id)}})
		print(messages)
		return self.prepare_result(messages)

	def get_messages_since_date(self, username, start_date):
		messages = self.collection.find({"username": username, "dt": {"$gt": start_date}})
		return self.prepare_result(messages)





def load_data_from_pgsql():
	import requests
	url = "http://127.0.0.1:9001/GetMessagesLast"
	
	messages = {
		"username": "admin",
		"command": "=============================================",
		"comment": "|||||||||||||||||||||||||||||||||||||||||||||",
		"data": "100000"
	}
	
	response = requests.post(url, json=messages)
	
	message_manager = MessageManager("mongodb://localhost:27017/", "Memer", "messages")
	message_manager.collection.delete_many({})
	for message in response.json():
		message_manager.save_message(	username='admin',
							   			icon_name=message['icon'],
										message_text=message['message'],
										hyperlink=message['hyperlink'],
										date=message['dt'])
		print(message)
	return response.json()






if __name__ == "__main__":
	# Инициализация менеджера сообщений
	message_manager = MessageManager("mongodb://localhost:27017/", "Memer", "messages")

	# Сохранение сообщения в базу данных
	# message_manager.save_message(username="Test", icon_name="first", message_text="Hello, world!4", hyperlink="https://example3.com")
	# message_manager.save_message(username="Test", icon_name="second", message_text="Hello, world!5", hyperlink="https://example4.com")
	# message_manager.save_message(username="Test", icon_name="third", message_text="Hello, world!6", hyperlink="https://example5.com")

	# Получение последних сообщений пользователя
	# last_messages = message_manager.get_last_messages("test", 5)
	# print("Last messages:")
	# for message in last_messages:
	# 	print(message)

	# messages_since_id = message_manager.get_messages_since_date("Test", datetime.now() - timedelta(hours=2))
	
	# since_message_id = ObjectId('662d04a64e01e7a079a8cce1')
	# messages_since_id = message_manager.get_messages_since_id("Test", since_message_id)
	# for message in messages_since_id:
	# 	print()
	# 	print(message)
	# print()
	# print({'count':len(messages_since_id)})

	




