from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config.cfg import psw, table, TOKEN
from aiogram import Bot, Dispatcher
from database.db import DataBase


db = DataBase(host='localhost', password=psw, database=table)
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())


