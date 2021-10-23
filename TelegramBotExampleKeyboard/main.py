"""
minimum viable product
"""
import ast
import logging

from aiogram import Dispatcher, Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils import executor


from TelegramBotExampleKeyboard.callback_data import items_callback
from config import TOKEN
from items import course

logging.basicConfig(format=u'%(filename)s #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO, )  # logging

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
                                                             callback_data=items_callback.new(item_id=f"{course.id}"))
                                    ],
                                    [
                                        InlineKeyboardButton(text="👍", callback_data="like"),
                                        InlineKeyboardButton(text="👎", callback_data="dislike")
                                    ],
                                    [
                                        InlineKeyboardButton(text="Поделиться с другом", callback_data="share"),
                                    ]
                                ])

@dp.message_handler(commands="items")
async def items_command(message: types.Message):
    await message.answer_photo(course.photo_url, caption='Курс!', reply_markup=keyboard, )




@dp.callback_query_handler(text_contains="buy")
async def item_buying(call: CallbackQuery):
    await call.answer(cache_time=60)

    callback_data = call.data
    logging.info(f"{callback_data=}")
    logging.info(f"{call=}")
    test=ast.literal_eval(callback_data)

    item_id = test.get()
    await call.message.edit_caption(f"Покупай товар номер {item_id}")
    await call.message.edit_reply_markup(reply_markup=None)



if __name__ == '__main__':
    executor.start_polling(dp)



@dp.callback_query_handler(items_callback.filter(item_name="apple"))
async def buying_apples(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)

    # Выведем callback_data и тут, чтобы сравнить с предыдущим вариантом.
    logging.info(f"{callback_data=}")

    quantity = callback_data.get("quantity")
    await call.message.answer(f"Вы выбрали купить яблоки. Яблок всего {quantity}. Спасибо.",
                              reply_markup=apples_keyboard)
