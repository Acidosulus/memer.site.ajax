import json
from click import echo, style

class UsersDataStorage():
	def __init__(self, dataFromAPI):
		echo(style(text='Data from APIServer:', fg='green') + style(text=dataFromAPI, fg='bright_green'))
		js = json.loads(dataFromAPI)
		self.data=js['users']

	# find and return user data by user_name
	def FindDataByUserName(self, user_name:str):
		result = {}
		for element in self.data:
			if element['name']==user_name:
				result = element
				break
		return result