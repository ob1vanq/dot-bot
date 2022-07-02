from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from app.filters.admin import AdminFilter
from app.states.admin import AdminSG


async def info(msg: Message):
    with open('.env', 'r', encoding='utf-8') as file:
        env = file.read()

    text = (
        'Send me <b>.env</b> file.\n\n<b>Current setting</b>:\n\n<pre>' + env + '</pre>'
    )
    await msg.answer(text)
    await AdminSG.File.set()


async def load_env(msg: Message, state: FSMContext):
    if msg.document.file_name.split('.')[-1] == 'env':
        await msg.document.download(destination='.env')
        await msg.answer('Successfully update settings')
    else:
        await msg.answer('Wrong file type')
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(info, AdminFilter(), Command('admin'), state='*')
    dp.register_message_handler(load_env, AdminFilter(), content_types=types.ContentType.DOCUMENT, state=AdminSG.File)