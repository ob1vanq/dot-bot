import re
from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import Config
from app.handlers.private.start import welcome_to_user
from app.keyboards.inline.menu import currency_kb, back_kb, pay_kb
from app.states.exchange import ExchangeSG

AMOUNT_REGEX = re.compile(
    r'^[+]?[0-9]*[.,]?[0-9]+(?:[eE][+]?[0-9]+)?$'
)


async def select_currency(call: CallbackQuery):
    text = (
        '<b>📊 Select currency you want to give</b>'
    )
    await call.message.edit_text(text, reply_markup=currency_kb)
    await ExchangeSG.Amount.set()


async def dot_to_doge(call: CallbackQuery, state: FSMContext):
    curr = Config.from_env().curr

    text = (
        'You want to exchange <b>DOT</b> to <b>DOGE</b>\n\n'
        f'Exchange rate: 1 DOT = <b>{curr.DOT_rate}</b> DOGE\n'
        f'The reserve is: <b>{curr.DOT_reserve}</b>\n\n'
        f'🔽 Minimum exchange amount DOT for DOGE = 1 DOT\n'
        f'🔼 Maximum exchange amount DOT for DOGE = 100000 DOT\n\n'
        f'<b>How much DOT would you like to give away?</b>'
    )
    msg = await call.message.edit_text(text, reply_markup=back_kb)
    await state.update_data(operation='dot-to-doge')  # dot-to-doge
    await ExchangeSG.Email.set()


async def doge_to_dot(call: CallbackQuery, state: FSMContext):
    curr = Config.from_env().curr

    text = (
        'You want to exchange <b>DOGE</b> to <b>DOT</b>\n\n'
        f'Exchange rate: 1 DOGE = <b>{curr.DOGE_rate}</b> DOT\n'
        f'The reserve is: <b>{curr.DOGE_reserve}</b>\n\n'
        f'🔽 Minimum exchange amount DOGE for DOT = 1 DOT\n'
        f'🔼 Maximum exchange amount DOGE for DOT = 100000 DOT\n\n'
        f'<b>How much DOGE would you like to give away?</b>'
    )
    msg = await call.message.edit_text(text, reply_markup=back_kb)
    await state.update_data(operation='doge-to-dot')
    await state.update_data(lst_msg_id=msg.message_id)
    await ExchangeSG.Email.set()


async def input_email(msg: Message, state: FSMContext):
    curr = Config.from_env().curr
    data = await state.get_data()
    operation = data.get('operation')
    amount = float(msg.text)

    if operation == 'dot-to-doge':
        convert = amount*curr.DOT_rate
        text = (
            f'You give: <b>{amount}</b> DOT\n'
            f'You will get: <b>{convert}</b> DOGE\n\n'
        )
    else:
        convert = amount*curr.DOGE_rate
        text = (
            f'You give: <b>{amount}</b> DOGE\n'
            f'You will get: <b>{convert}</b> DOT\n\n'
        )

    text += f'📧 Please enter your E-mail box: example@gmail.com\n'

    msg = await msg.answer(text=text, reply_markup=back_kb)
    await state.update_data(text=text, amount=amount, convert=convert, lst_msg_id=msg.message_id)
    await ExchangeSG.Wallet.set()


async def input_wallet(msg: Message, state: FSMContext):
    data = await state.get_data()
    operation = (data.get('operation')).split('-')[-1].upper()
    text = (
        f'Enter Wallet {operation} to receive\n'
        'For example: <i>TwwjPsuybffw12Ul3MK3fcTBX4O1Es41Tg</i>'
    )
    await msg.answer(text)
    await state.update_data(email=msg.text)
    await ExchangeSG.Tag.set()


async def input_wallet_tag(msg: Message, state: FSMContext):
    data = await state.get_data()
    operation = (data.get('operation')).split('-')[-1].upper()
    text = (
        f'Enter Wallet tag {operation}\n'
    )
    await msg.answer(text)
    await state.update_data(wallet=msg.text)
    await ExchangeSG.Show.set()


async def show_data(msg: Message, state: FSMContext):
    curr = Config.from_env().curr
    data = await state.get_data()
    operation = data.get('operation')
    op_from = operation.split('-')[0].split('-')[0].upper()
    op_to = operation.split('-')[-1].upper()
    amount = data.get('amount')
    convert = data.get('convert')
    email = data.get('email')
    wallet = data.get('wallet')
    wallet_tag = msg.text
    await msg.answer(f'<b><pre>{curr.wallet_address}</pre></b>')
    text = (
        '❗️<b>Attention</b>❗️\n'
        'You should press the "I paid" button only after payment, and the\n'
        'process of creating an application can also be interrupted by\n'
        'clicking on the "Cancel" button.\n\n'
        f'<b>Open the client and make a transfer by details</b>\n\n'
        # f'Wallet address:'
    )
    lmsg = await msg.answer(text=text, reply_markup=pay_kb)

    date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    text = (
        f'Operation <b>{operation.upper()}</b>\n\n'
        f'Order date: <pre>{date}</pre>\n\n'
        f'<b>{amount} {op_from}</b> to <b>{convert} {op_to}</b>\n\n'
        f'Email: {email}\n'
        f'Wallet: {wallet}\n'
        f'Tag: {wallet_tag}\n\n'
    )
    # lmsg = await msg.answer(text=text, reply_markup=pay_kb)
    await state.update_data(wallet_tag=wallet_tag, date=date, lst_msg_id=lmsg.message_id, text=text, mention=msg.from_user.get_mention())


async def send_admin(call: CallbackQuery, state: FSMContext):
    conf = Config.from_env()
    data = await state.get_data()
    operation = data.get('operation')
    op_from = operation.split('-')[0].split('-')[0].upper()
    op_to = operation.split('-')[-1].upper()
    amount = data.get('amount')
    convert = data.get('convert')
    email = data.get('email')
    wallet = data.get('wallet')
    wallet_tag = data.get('wallet_tag')
    mention = data.get('mention')
    lst_msg_id = data.get('lst_msg_id')
    date = data.get('date')
    order_text = data.get('text')

    text = (
        f'<b>User [{mention}] pay operation\n\n</b>'
        f'Operation <b>{operation.upper()}</b>\n\n'
        f'Order date: <b>{date}</b>\n\n'
        f'<b>{amount} {op_from}</b> to <b>{convert} {op_to}</b>\n\n'
        f'Email: {email}\n'
        f'Wallet: <pre>{wallet}</pre>\n'
        f'Tag: <pre>{wallet_tag}</pre>\n\n'
    )
    await call.message.answer(order_text)
    await call.bot.edit_message_reply_markup(reply_markup=None, chat_id=call.from_user.id, message_id=lst_msg_id)
    await call.answer(show_alert=True, text='Your data has been sent to the administration. Thank you')

    for admin_id in conf.bot.admin_ids:
        await call.bot.send_message(text=text, chat_id=admin_id)
    await state.reset_data()
    await state.finish()

    await welcome_to_user(call.message)


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(select_currency, text='exchange', state='*')
    dp.register_callback_query_handler(dot_to_doge, text='dot-to-doge', state=ExchangeSG.Amount)
    dp.register_callback_query_handler(doge_to_dot, text='doge-to-dot', state=ExchangeSG.Amount)
    dp.register_message_handler(input_email, state=ExchangeSG.Email, regexp=AMOUNT_REGEX)
    dp.register_message_handler(input_wallet, state=ExchangeSG.Wallet)
    dp.register_message_handler(input_wallet_tag, state=ExchangeSG.Tag)
    dp.register_message_handler(show_data, state=ExchangeSG.Show)
    dp.register_callback_query_handler(send_admin, state=ExchangeSG.Show)

    # back to
    dp.register_callback_query_handler(back_to_select_currency, state=ExchangeSG.Email)
    dp.register_callback_query_handler(back_to_near_to_xpr, state=ExchangeSG.Wallet)
    dp.register_callback_query_handler(back_to_input_email, state=ExchangeSG.Tag)


async def back_to_select_currency(call: CallbackQuery, state: FSMContext):
    await select_currency(call)


async def back_to_near_to_xpr(call: CallbackQuery, state: FSMContext):
    await dot_to_doge(call, state)


async def back_to_input_email(call: CallbackQuery, state: FSMContext):
    await input_email(call.message, state)
