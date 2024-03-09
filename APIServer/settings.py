import configparser 
import sys

class Options:
	def __init__(self, path:str):
		self.config = configparser.ConfigParser()
		self.config.read(path)
		self.SELF_ADRESS = self.config[sys.platform]["webserver"]
		self.API_ADRESS = self.config[sys.platform]["apiserver"]
		self.LANDDBURI = self.config[sys.platform]["langdb"]
		self.SECRET_KEY = self.config[sys.platform]["SECRET_KEY"]
		print(f'SELF_ADRESS:{self.SELF_ADRESS}')
		print(f'API_ADRESS:{self.API_ADRESS}')
		print(f'LANDDBURI:{self.LANDDBURI}')
