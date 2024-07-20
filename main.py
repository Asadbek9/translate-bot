import typing_extensions
from googletrans import Translator
import asyncio

translator = Translator()


from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F, Dispatcher, types, Bot, filters
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Language(StatesGroup):
    lang1 = State()
    lang2 = State()


choose_language = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Translate to Uzbek"), KeyboardButton(text="Translate to Russian")]
], resize_keyboard=True)

bot = Bot(token="7131462432:AAFG2RBv_5yJSEH223Gi3EsLnpDvUSoVq7w")
dp = Dispatcher(bot=bot)


@dp.message(filters.Command("start"))
async def start_func(message: types.Message):
    await message.answer(f"Xush kelibsiz {message.from_user.full_name}", reply_markup=choose_language)


@dp.message(F.text == "Translate to Russian")
async def rus_lang(message: types.Message, state: FSMContext):
    await state.set_state(Language.lang1)
    await message.answer("What do you want to translate?")


@dp.message(Language.lang1)
async def first_name_rus(message: types.Message, state: FSMContext):
    await state.update_data(lang1=message.text)
    text = translator.translate(text=f"{message.text}", dest="ru")

    await message.answer(text.text)


@dp.message(F.text == "Translate to Uzbek")
async def uzb_lang(message: types.Message, state: FSMContext):
    await state.set_state(Language.lang2)
    await message.answer("What do you want to translate?")


@dp.message(Language.lang2)
async def uzb_translate(message: types.Message, state: FSMContext):
    await state.update_data(lang2=message.text)
    text = translator.translate(text=f"{message.text}", dest="uz")

    await message.answer(text.text)





async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

