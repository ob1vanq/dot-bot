from .base import *

start_kb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Exchange 💸', callback_data='exchange')],
        [InlineKeyboardButton(text='Support 📨', callback_data='support')]
    ]
)

back_bt = InlineKeyboardButton(text='🔙 back', callback_data='back')
back_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[back_bt]])


pay_kb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='I paid ✅', callback_data='paid')],
        [InlineKeyboardButton(text='Cancel', callback_data='cancel')]
    ]
)

currency_kb = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='DOT to DOGE', callback_data='dot-to-doge'),
            InlineKeyboardButton(text='DOGE to DOT', callback_data='doge-to-dot')
        ],
        [back_bt]
    ]
)