from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def get_limit_inline_keyboard() -> InlineKeyboardMarkup:
    # Создаем клавиатуру с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="10", callback_data="limit_10"),
            InlineKeyboardButton(text="25", callback_data="limit_25"),
        ],
        [
            InlineKeyboardButton(text="50", callback_data="limit_50"),
            InlineKeyboardButton(text="100", callback_data="limit_100"),
        ],
        [
            InlineKeyboardButton(text="150", callback_data="limit_150"),
            InlineKeyboardButton(text="250", callback_data="limit_250"),
        ],
        [
            InlineKeyboardButton(text="Отменить настройку", callback_data="cancel"),
        ]
    ])

    return keyboard

def get_take_profit_keyboard() -> InlineKeyboardMarkup:
    # Создаем кнопки
    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1%", callback_data="profit_1"),
        InlineKeyboardButton(text="2%", callback_data="profit_2")
         ],
        [
            InlineKeyboardButton(text="3%", callback_data="profit_3"),
        InlineKeyboardButton(text="5%", callback_data="profit_5")
        ],
        [
            InlineKeyboardButton(text="7%", callback_data="profit_7"),
        InlineKeyboardButton(text="10%", callback_data="profit_10")
        ],
        [
            InlineKeyboardButton(text="Отменить настройку", callback_data="cancel")
        ],
    ])

    return buttons


def get_stop_lose_keyboard() -> InlineKeyboardMarkup:
    # Создаем кнопки
    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1%", callback_data="stop_1"),
        InlineKeyboardButton(text="2%", callback_data="stop_2")
         ],
        [
            InlineKeyboardButton(text="3%", callback_data="stop_3"),
        InlineKeyboardButton(text="4%", callback_data="stop_4")
        ],
        [
            InlineKeyboardButton(text="Отменить настройку", callback_data="cancel")
        ],
    ])

    return buttons


def get_time_frame_keyboard() -> InlineKeyboardMarkup:

    # Создаем кнопки
    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="5m", callback_data="time_5m"),
        InlineKeyboardButton(text="10m", callback_data="time_10m")
         ],
        [
            InlineKeyboardButton(text="15m", callback_data="time_15m"),
        InlineKeyboardButton(text="30m", callback_data="time_30m")
        ],
        [
            InlineKeyboardButton(text="60m", callback_data="time_60m"),
        InlineKeyboardButton(text="Отменить настройку", callback_data="cancel")
        ],
    ])

    return buttons


def get_count_frame_keyboard() -> InlineKeyboardMarkup:

    # Создаем кнопки
    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="2 свечи", callback_data="count_2"),
        InlineKeyboardButton(text="3 свечи", callback_data="count_3")
        ],
        [
            InlineKeyboardButton(text="4 свечи", callback_data="count_4"),
        InlineKeyboardButton(text="5 свечи", callback_data="count_5")
        ],
        [
            InlineKeyboardButton(text="Отменить настройку", callback_data="cancel")
        ],
    ])

    return buttons


def get_deposit_keyboard() -> InlineKeyboardMarkup:

    # Создаем кнопки
    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1 usdt", callback_data="dep_1"),
        InlineKeyboardButton(text="5 usdt", callback_data="dep_5")
         ],
        [
            InlineKeyboardButton(text="10 usdt", callback_data="dep_10"),
        InlineKeyboardButton(text="25 usdt", callback_data="dep_25")
         ],
        [
            InlineKeyboardButton(text="50 usdt", callback_data="dep_50"),
        InlineKeyboardButton(text="Отменить настройку", callback_data="cancel")
        ],
    ])

    return buttons


def get_rsi_keyboard() -> InlineKeyboardMarkup:

    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="RSI 25", callback_data="rsi_25"),
        InlineKeyboardButton(text="RSI 30", callback_data="rsi_30")
         ],
        [
            InlineKeyboardButton(text="RSI 35", callback_data="rsi_35"),
        InlineKeyboardButton(text="RSI 40", callback_data="rsi_40")
         ],
        [
            InlineKeyboardButton(text="RSI 45", callback_data="rsi_45"),
            InlineKeyboardButton(text="RSI 50", callback_data="rsi_50")
        ],
        [
            InlineKeyboardButton(text="RSI 55", callback_data="rsi_55"),
            InlineKeyboardButton(text="RSI 60", callback_data="rsi_60")
        ],
        [
            InlineKeyboardButton(text="RSI 65", callback_data="rsi_65"),
            InlineKeyboardButton(text="RSI 70", callback_data="rsi_70"),
        ],
        [
            InlineKeyboardButton(text="Отменить настройку", callback_data="cancel")
        ],
    ])

    return buttons