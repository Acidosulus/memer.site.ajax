import configparser
from click import echo, style

config = configparser.ConfigParser()
config.read("options.ini")

token=config["notifier_bot"]["token"]


