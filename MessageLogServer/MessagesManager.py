from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime, timedelta
from rich import print




class MessageManager:
	def __init__(self, db_url, db_name, collection_name):
		self.client = MongoClient(db_url)
		self.db = self.client[db_name]
		self.collection = self.db[collection_name]

	def save_message(self, username, icon_name, message_text, hyperlink):
		message = {
			"username": username,
			"date": datetime.now(),
			"icon_name": icon_name,
			"message_text": message_text,
			"hyperlink": hyperlink
		}
		self.collection.insert_one(message)

	def get_last_messages(self, username, num_messages):
		messages = self.collection.find({"username": username}).sort("date", -1).limit(num_messages)
		return list(messages)

	def get_messages_since_id(self, username, message_id):
		messages = self.collection.find({"username": username, "_id": {"$gt": message_id}})
		return list(messages)

	def get_messages_since_date(self, username, start_date):
		messages = self.collection.find({"username": username, "date": {"$gt": start_date}})
		return list(messages)

# Пример использования
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
	
	# Получение сообщений пользователя с идентификатором больше заданного
	since_message_id = ObjectId('662d04a64e01e7a079a8cce1') # Предположим, что это идентификатор сообщения
	messages_since_id = message_manager.get_messages_since_id("Test", since_message_id)
	
	# print("Messages since message ID", since_message_id, ":")
	for message in messages_since_id:
		print()
		print(message)
	print()
	print({'count':len(messages_since_id)})