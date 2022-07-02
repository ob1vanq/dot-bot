from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from app.keyboards.inline.menu import start_kb, back_kb


async def welcome_to_user(msg: Message):
    text = (
        '<b>Welcome to DOT_EXCHANGE_BOT</b>\n\n'
        'Our bot will help you quickly and reliably convert cryptocurrency\n\n'
        '<b>📲 Benefits of our service:</b>\n'
        '✔️ Operational support 24/7\n'
        '✔️ Automatic exchange\n'
        '✔️ Favorable exchange rate'
    )
    await msg.answer(text, reply_markup=start_kb)


async def support(call: CallbackQuery):
    await call.message.delete()
    text = (
        'Telegram: @dot_exchange_support\n'
        'Email: dot_exchange@yahoo.com'
    )
    await call.message.answer(text=text, reply_markup=back_kb)


async def cancel(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.reset_data()
    await state.finish()
    await welcome_to_user(call.message)


def setup(dp: Dispatcher):
    dp.register_message_handler(welcome_to_user, CommandStart(), state='*')
    dp.register_callback_query_handler(support, text='support', state='*')
    dp.register_callback_query_handler(cancel, text=['back', 'cancel'], state='*')
