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


	def save_message(self, username, icon_name, message_text, hyperlink):
		message = {
			"username": username,
			"dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"icon": icon_name,
			"message": message_text,
			"hyperlink": hyperlink
		}
		self.collection.insert_one(message)

	def get_last_messages(self, username, num_messages):

		today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
		yesterday = today - timedelta(days=1)

		messages = self.collection.find({	"username": username,
    										"dt": {"$gte": yesterday, "$lt": today}}).sort("dt", 1)

		return self.prepare_result(messages)




if __name__ == "__main__":
	message_manager = MessageManager("mongodb://localhost:27017/", "Memer", "messages")
