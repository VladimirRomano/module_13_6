from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать'),
                                    KeyboardButton(text='Информация')]], resize_keyboard=True)


but = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
                                             InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]])


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=but)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) + 5')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    Calories = 10 * (data['weight']) + 6.25 * (data['growth']) - 5 * (data['age']) + 5
    await message.answer(f'Расчитанное количество каллорий: {Calories}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет', reply_markup=kb)


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)