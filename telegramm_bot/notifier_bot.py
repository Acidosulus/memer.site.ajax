import configparser
from click import echo, style
import asyncio
from aiogram import Bot, Dispatcher, types


class Telegram_Notifier():

	def __init__(self):
		config = configparser.ConfigParser()
		config.read("options.ini")
		self.token = config["notifier_bot"]["token"]
		echo(f"""{style(text='token', bg='blue', fg='yellow')} {style(text='token', bg='blue', fg='yellow')}""")
		bot = Bot(token='YOUR_BOT_TOKEN')
		dp = Dispatcher(bot)

	async def send_notification(self, user_id, message):
		await self.bot.send_message(user_id, message)