"""
minimum viable product
"""

import logging
import typing

from aiogram import Dispatcher, Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

from callback_data import items_callback
from config import TOKEN
from items import course

logging.basicConfig(level=logging.INFO)  # logging

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)  # initialize the bot


@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    await message.answer("Привет!\nБот создан для практики и выполнения задания курса")


# Keyboard with inline buttons

keyboard = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="Купить товар",
                                                             callback_data=items_callback.new(action="buy",
                                                                                              item_id=f"{course.id}"))
                                    ],
                                    [
                                        InlineKeyboardButton(text="👍", callback_data="like"),
                                        InlineKeyboardButton(text="👎", callback_data="dislike")
                                    ],
                                    [
                                        InlineKeyboardButton(text="Поделиться с другом", callback_data="share"),
                                    ]
                                ])


# /items Handler
@dp.message_handler(commands="items")
async def items_command(message: types.Message):
    await message.answer_photo(course.photo_url, caption='Курс!', reply_markup=keyboard)


# callback handler for first button
@dp.callback_query_handler(items_callback.filter(action="buy"))
async def buying_item(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    await call.answer(cache_time=60)

    item_id = callback_data.get("item_id")
    await call.message.edit_caption(f"Покупай товар номер {item_id}", reply_markup=None)


if __name__ == '__main__':
    executor.start_polling(dp)
