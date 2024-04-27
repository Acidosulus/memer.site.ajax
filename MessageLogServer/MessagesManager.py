from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime, timedelta

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
	# message_manager.save_message(username="Test", icon_name="smiley", message_text="Hello, world!", hyperlink="https://example.com")
	# message_manager.save_message(username="Test", icon_name="sad", message_text="Hello, world!2", hyperlink="https://example1.com")
	# message_manager.save_message(username="Test", icon_name="welcome", message_text="Hello, world!3", hyperlink="https://example2.com")

	# Получение последних сообщений пользователя
	last_messages = message_manager.get_last_messages("test", 5)
	print("Last messages:")
	for message in last_messages:
		print(message)

	# Получение сообщений пользователя с идентификатором больше заданного
	since_message_id = 100 # Предположим, что это идентификатор сообщения
	messages_since_id = message_manager.get_messages_since_date("JohnDoe", datetime.now() - timedelta(hours=6))
	print("Messages since message ID", since_message_id, ":")
	for message in messages_since_id:
		print(message)