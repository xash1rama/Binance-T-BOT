from binance.um_futures import UMFutures
from dotenv import load_dotenv
import os
import requests
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from database import Orders, Base, engine
from setup import create_datas
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboard import get_limit_inline_keyboard, get_rsi_keyboard, get_take_profit_keyboard, get_stop_lose_keyboard, get_time_frame_keyboard, get_count_frame_keyboard, get_deposit_keyboard
from metrix import *

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHANEL = os.getenv("TG_CHANEL")



bot = Bot(token=TG_TOKEN)

# Создаем экземпляр хранилища
storage = MemoryStorage()

# Создаем экземпляр Dispatcher
dp = Dispatcher(storage=storage)

# Подключаем роутер (если он есть)
router = Router()
dp.include_router(router)

client = UMFutures(key=API_KEY, secret=API_SECRET)

is_running = False


class Form(StatesGroup):
    limit = State()
    take_profit = State()
    stop_lose = State()
    time_frame = State()
    count_frame = State()
    deposit = State()
    rsi = State()


def send_message(text):
    response = requests.post(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        json={"chat_id": TG_CHANEL, "text": text},
    )


@dp.message(Command("start"))
async def send_welcome(message: types.Message):

    text = """
🤖T-Bot
🪪Инструкция🪪:

/balance - 💰Посмотреть баланс
/check - 📫 Посмотреть открытую позицию
/info - ♟ Узнать о моей стратегииторговли
/settings_now - 📁 Как настроен бот
/stop_all - 🛑 Закрыть все позиции 
/run - 🟩 Запустить бота
/settings - 🛠 Установить новые значение для бота
/top_coins - 🪙 Топ монет которые будут сейчас в списке поиска входа
"""
    await message.answer(text)


@dp.message(Command("info"))
async def top_coins(message: types.Message):
    try:

        text = """
🟩Стратегия динамического анализа с использованием индикаторов🟩

Описание стратегии:
1. Динамический анализ:
Стратегия основывается на анализе текущих рыночных условий с помощью различных индикаторов, таких как RSI (Индекс относительной силы) и RA (Рынок/Анализ). Это позволяет принимать обоснованные решения о входе и выходе из позиций.

2. Индикаторы:

RSI: Используется для определения силы тренда. Значения ниже 30 указывают на перепроданность, а выше 70 — на перекупленность. Ваша стратегия предполагает использование значения RSI не выше 50 для более безопасной торговли.
RA: Этот индикатор помогает определить, когда цена актива может развернуться, основываясь на его предыдущих значениях.

3. Управление рисками:
Стратегия включает установку уровней Take Profit и Stop Loss для защиты капитала. Это позволяет фиксировать прибыль при достижении заданного уровня и ограничивать убытки в случае неблагоприятного движения рынка.

4. Использование маржинальной торговли:
Вы открываете позиции на фьючерсах, используя средства в USDT, что позволяет вам контролировать большие объемы активов, чем у вас есть на счету, благодаря левериджу.

5. Адаптивность:
Стратегия учитывает текущие рыночные условия и динамически адаптируется, выбирая топовые монеты для торговли на основе их активности и анализа трендов.

6. Автоматизация:
Система полностью автоматизирована, что позволяет минимизировать человеческий фактор и быстро реагировать на изменения в рынке.

Наша стратегия сочетает в себе элементы технического анализа и управления рисками, что делает её подходящей для активной торговли на фьючерсах.
Она направлена на поиск выгодных точек входа и выхода, основываясь на анализе исторических данных и текущих рыночных условий.
Это позволяет вам эффективно управлять своим капиталом и минимизировать риски. 😊
        """
        await message.answer(text)
        await message.answer("/start - 📋 Все команды ")

    except Exception as e:
        await message.answer(
                f"""
Произошла ошибка:  + {str(e)}

/start - 📋 Все команды 
        """)


@dp.message(Command("top_coins"))
async def top_coins(message: types.Message):
    try:
        top = session.query(Information).filter(Information.name == "Лимит токенов").first().data
        top_coins_list = get_top_coins()
        # Преобразуем список монет в строку
        text = f" У вас задан Топ-{top} монет:\n" + "🐃".join(top_coins_list)
        await message.answer(text)
        await message.answer("/start - 📋 Все команды ")

    except Exception as e:
        await message.answer(
                f"""
Произошла ошибка:  + {str(e)}

/start - 📋 Все команды 
        """)


@dp.message(Command("balance"))
async def balance(message: types.Message):
    try:
        global trading_bot


        text = f"""
Баланс: {trading_bot.check_balance()} USDT

/start - 📋 Все команды 
"""
        await message.answer(text)

    except Exception as e:
        await message.answer(
                f"""
Произошла ошибка:  + {str(e)}

/start - 📋 Все команды 
        """)


@dp.message(Command("check"))
async def check(message: types.Message):
    try:
        global trading_bot
        position = trading_bot.open_position
        if position:
            text = f"""
Открыта позиция на {trading_bot.open_position.symbol}
Объем: {trading_bot.open_position.volume}
TP: {trading_bot.open_position.take_profit}
SL: {trading_bot.open_position.stop_loss}

/start - 📋 Все команды 
"""
        else:
            text = f"""
Открытых позиций нет!
            
/start - 📋 Все команды 
            """
        await message.answer(text)

    except Exception as e:
        await message.answer(
                f"""
Произошла ошибка: {str(e)}

/start - 📋 Все команды 
        """)


@dp.message(Command("run"))
async def start_trading(message: types.Message):
    global is_running, trading_bot

    if not is_running:
        is_running = True
        await message.answer("""
Начинаю свою деятельность! 🚀
        
/top_coins - список криптовалют сегодня
/stop_all - закрыть позицию/выключить поиск""")
        await trading_bot.trade_logic()  # Запускаем торговую логику
    else:
        if trading_bot.check_open_positions():
            await message.answer(f"""
Я уже контролирую валюту! 
Есть открытая позиция!
                
Монета: {trading_bot.open_position.symbol}
Объем: {trading_bot.open_position.volume}
Закрыть +: {trading_bot.open_position.take_profit}
Закрыть -: {trading_bot.open_position.stop_loss}
                
/top_coins - 🪙 список криптовалют сегодня
/stop_all - закрыть позицию/выключить поиск
(Если позиция не закрылась лучше закрыть вручную на бирже)
""")
        else:
            await message.answer("""
Я начал свою деятельность! 🚀
Идет поиск точки входа! 
                    
/top_coins - 🪙 список криптовалют сегодня
/stop_all - закрыть позицию/выключить поиск""")



@dp.message(Command("stop_all"))
async def stop_all_trading(message: types.Message):
    global is_running
    if is_running:
        trading_bot.close_all_positions()
        is_running = False
        await message.answer("""
Все открытые позиции распроданы. Я остановливаю свою работу. 🛑
        
/run - 🟩 Запустить бота
/start - 📋 Все команды 
        """)
    else:
        trading_bot.close_all_positions()
        await message.answer("""
Я не работаю в данный момент.
        
/run - 🟩 Запустить бота
/start - 📋 Все команды 
""")


@dp.message(Command("settings_now"))
async def stop_all_trading(message: types.Message):
    tp = session.query(Information).filter(Information.name == "Take profit").first().data
    sl = session.query(Information).filter(Information.name == "Stop lose").first().data
    await message.answer(f"""
   🛠🤖 Настройки Бота 🤖🛠

Бот ищет токены из топ - {session.query(Information).filter(Information.name == "Лимит токенов").first().data } активных монет за 24ч
Take profit (точка выхода) на - {round(float(tp) * 100, 2)} % роста 📈
Stop lose (точка выхода при подении) - {round(float(sl) * 100, 2)} % упадка 📉
Time frame (свечи) -{session.query(Information).filter(Information.name == "Time Frame").first().data} 📊
Count frame (сколько свечей смотрим) - {session.query(Information).filter(Information.name == "Count frame").first().data} 🕯 
RSI (относительная сила) - {session.query(Information).filter(Information.name == "RSI").first().data} 🐃 
Deposit (ставка) - {session.query(Information).filter(Information.name == "Deposit").first().data}$ 💵 

/start - 📋 Все команды 
""")


@dp.message(Command("settings"))
async def start_settings(message: types.Message, state: FSMContext):
    try:
        await state.set_state(Form.limit)  # Устанавливаем состояние для имени
        limit_value = session.query(Information).filter(Information.name == "Лимит токенов").first()

        if limit_value:
            await message.answer(f"""
‼️‼️‼️
Я даю только свои варианты так как это предохранитель против фомо и человеских факторов!
Нельзя забывать о аккуратной торговле, малых процентах, не больших ставках и отcлеживании метрик!
‼️‼️‼️

Токены фильтрую по активности и выбираю топ лучших.
Ввыбери количество монет для поиска (сейчас: {limit_value.data}):
            """, reply_markup=get_limit_inline_keyboard())
        else:
            await message.answer("Не удалось получить лимит токенов из базы данных. /start")
    except Exception as e:
        await message.answer(f"""
Произошла ошибка: {str(e)}

/start - 📋 Все команды 
""")


@router.callback_query(StateFilter(Form.limit))  # Используйте StateFilter для ограничения состояния
async def process_limit(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
    try:
        profit_value = session.query(Information).filter(Information.name == "Take profit").first().data
        if callback_query.data == "cancel":
            await state.clear()  # Завершаем состояние
            await callback_query.message.answer(
                """
Изменение данных отменено!
        
Бот останется со старыми данными.
/settings_now - 📁 Как нстроен бот
/start - 📋 Все команды 
                """)
        else:
            limit = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
            await state.update_data(limit=limit)  # Сохраняем лимит в состоянии
            await callback_query.answer()  # Подтверждаем нажатие кнопки
            await state.set_state(Form.take_profit)  # Переходим к следующему состоянию
            await (callback_query.message if callback_query else message).answer(
                f"""
При достежении определенного уровня дохода я буду фиксировать прибыль!
                
Выбери процент роста при котором мне выходить из позиции (сейчаc: {round(float(profit_value) * 100 , 2)}%):""",
                reply_markup=get_take_profit_keyboard(),
            )

    except Exception as e:
        await state.clear()  # Завершаем состояние
        if callback_query:
            await callback_query.message.answer(
                f"""
Произошла ошибка: {str(e)}

/start - 📋 Все команды 
""")
        else:
            await message.answer(
                f"""
Произошла ошибка: {str(e)}

/start - 📋 Все команды 
""")


@router.callback_query(StateFilter(Form.take_profit))
async def process_profit(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
    try:
        stop_value = session.query(Information).filter(Information.name == "Stop lose").first().data
        if callback_query.data == "cancel":
            await state.clear()  # Завершаем состояние
            await callback_query.answer("Изменение данных отменено!")  # Подтверждаем нажатие кнопки
            await callback_query.message.answer(
                """
Изменение данных отменено!

Бот останется со старыми данными.
/settings_now - 📁 Как нстроен бот
/start - 📋 Все команды 
                """)
        else:
            profit = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
            await state.update_data(take_profit=profit)  # Сохраняем лимит в состоянии
            await callback_query.answer()  # Подтверждаем нажатие кнопки
            await state.set_state(Form.stop_lose)  # Переходим к следующему состоянию
            await (callback_query.message if callback_query else message).answer(

                f"""
Если рынок развернет свое направление то нужно будет выйти из позиции с небольшими потерями так что я ставлю Stop lose!
                
Выбери процент падения при котором мне выйти из позиции (сейчас: {round(float(stop_value) * 100 , 2)}%):""",
                reply_markup=get_stop_lose_keyboard(),
            )

    except Exception as e:
        await state.clear()  # Завершаем состояние
        if callback_query:
            await callback_query.message.answer(
                f"""
Произошла ошибка:  + {str(e)}

/start - 📋 Все команды 
""")
        else:
            await message.answer(
                f"""
Произошла ошибка:  + {str(e)}

/start - 📋 Все команды 
""")


@router.callback_query(StateFilter(Form.stop_lose))
async def process_stop(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
    try:
        time_value = session.query(Information).filter(Information.name == "Time Frame").first().data
        if callback_query.data == "cancel":
            await state.clear()  # Завершаем состояние
            await callback_query.answer("Изменение данных отменено!")  # Подтверждаем нажатие кнопки
            await callback_query.message.answer(
                """
Изменение данных отменено!

Бот останется со старыми данными.
/settings_now - 📁 Как нстроен бот
/start - 📋 Все команды 
                """)
        else:
            stop = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
            await state.update_data(stop_lose=stop)  # Сохраняем лимит в состоянии
            await callback_query.answer()  # Подтверждаем нажатие кнопки
            await state.set_state(Form.time_frame)  # Переходим к следующему состоянию
            await (callback_query.message if callback_query else message).answer(
                f"""
Я буду смотреть статистику последних свечей, вам нужно выбрать Time frame каждой свечи!
Анализ тенденций: Разные временные интервалы позволяют увидеть различные тенденции!
                
Выбери временные интервалы для свечей (сейчас: {time_value}):""",
                reply_markup=get_time_frame_keyboard(),
            )
    except Exception as e:
        await state.clear()  # Завершаем состояние
        if callback_query:
            await callback_query.message.answer(
                f"""
Произошла ошибка:  + {str(e)}

/start - 📋 Все команды 
""")
        else:
            await message.answer(
                f"""
Произошла ошибка:  + {str(e)}

/start - 📋 Все команды 
""")


@router.callback_query(StateFilter(Form.time_frame))
async def process_time(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
    try:
        count_value = session.query(Information).filter(Information.name == "Count frame").first().data
        if callback_query.data == "cancel":
            await state.clear()  # Завершаем состояние
            await callback_query.answer()  # Подтверждаем нажатие кнопки
            await callback_query.message.answer(
                """
Изменение данных отменено!

Бот останется со старыми данными.
/settings_now - 📁 Как нстроен бот
/start - 📋 Все команды 
                """)
        else:
            time = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
            await state.update_data(time_frame=time)  # Сохраняем лимит в состоянии
            await callback_query.answer()  # Подтверждаем нажатие кнопки
            await state.set_state(Form.count_frame)  # Переходим к следующему состоянию
            await (callback_query.message if callback_query else message).answer(
                f"""
Я буду смотреть что бы последние свези закрывались в плюс относительно друг друга!
                
Выбери какое количество свечей мне смотреть перед входом в позицию (сейчас: {count_value}):""",
                reply_markup=get_count_frame_keyboard(),
            )
    except Exception as e:
        await state.clear()  # Завершаем состояние
        if callback_query:
            await callback_query.message.answer(
                f"""
Произошла ошибка:  + {str(e)}

/start - 📋 Все команды 
""")
        else:
            await message.answer(
                f"""
Произошла ошибка:  + {str(e)}

/start - 📋 Все команды 
""")


@router.callback_query(StateFilter(Form.count_frame))
async def process_count(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
    try:
        rsi_value = session.query(Information).filter(Information.name == "RSI").first().data
        if callback_query.data == "cancel":
            await state.clear()  # Завершаем состояние
            await callback_query.answer()  # Подтверждаем нажатие кнопки
            await callback_query.message.answer(
                """
Изменение данных отменено!

Бот останется со старыми данными.
/settings_now - 📁 Как нстроен бот
/start - 📋 Все команды 
                """)
        else:
            count = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
            await state.update_data(count_frame=count)  # Сохраняем лимит в состоянии
            await callback_query.answer()
            await state.set_state(Form.rsi)  # Переходим к следующему состоянию
            await (callback_query.message if callback_query else message).answer(
                f"""
О.

Выбери уровень RSI - показатель относительной силы покупателей/продавцов.
Где 30 - большая сила у покупателей, 70 - большая сила у продавцов.
Для стратегии которую мы поодерживаем будет более безопасно не выбирать более 50.

Выбери необходимый показатель (сейчас: {rsi_value}):""",
                reply_markup=get_rsi_keyboard(),)
    except Exception as e:
        await state.clear()
        if callback_query:
            await callback_query.message.answer(
                f"""
Произошла ошибка: {str(e)}

/start - 📋 Все команды 
""")
        else:
            await message.answer(
                f"""
Произошла ошибка: {str(e)}

/start - 📋 Все команды 
""")


@router.callback_query(StateFilter(Form.rsi))
async def process_count(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
    try:
        dep_value = session.query(Information).filter(Information.name == "Deposit").first().data
        if callback_query.data == "cancel":
            await state.clear()  # Завершаем состояние
            await callback_query.answer()  # Подтверждаем нажатие кнопки
            await callback_query.message.answer(
                """
Изменение данных отменено!

Бот останется со старыми данными.
/settings_now - 📁 Как нстроен бот
/start - 📋 Все команды 
                """)
        else:
            rsi = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
            await state.update_data(rsi=rsi)  # Сохраняем лимит в состоянии
            await callback_query.answer()
            await state.set_state(Form.deposit)  # Переходим к следующему состоянию
            await (callback_query.message if callback_query else message).answer(
                f"""
Я буду входить в позицию строго на определенную сумму.
                
Выбери депозит с которым входить в позицию (сейчас: {dep_value}$):""",
                reply_markup=get_deposit_keyboard(),)
    except Exception as e:
        await state.clear()  # Завершаем состояние
        if callback_query:
            await callback_query.message.answer(
                f"""
Произошла ошибка:  + {str(e)}

/start - 📋 Все команды 
""")
        else:
            await message.answer(
                f"""
Произошла ошибка:  + {str(e)}

/start - 📋 Все команды 
""")


@router.callback_query(StateFilter(Form.deposit))
async def process_dep(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
    try:
        if callback_query.data == "cancel":
            await state.clear()  # Завершаем состояние
            await callback_query.answer()  # Подтверждаем нажатие кнопки
            await callback_query.message.answer(
                """
Изменение данных отменено!

Бот останется со старыми данными.
/settings_now - 📁 Как нстроен бот
/start - 📋 Все команды 
                """)
        else:
            dep = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
            await state.update_data(deposit=dep)  # Сохраняем лимит в состоянии
            await callback_query.answer()
            await state.set_state(Form.take_profit)  # Переходим к следующему состоянию

            # Получаем все данные
            data = await state.get_data()
            old_limit = session.query(Information).filter(Information.name == "Лимит токенов").first()
            old_take_profit = session.query(Information).filter(Information.name == "Take profit").first()
            old_stop_lose = session.query(Information).filter(Information.name == "Stop lose").first()
            old_time_frame = session.query(Information).filter(Information.name == "Time Frame").first()
            old_count_frame = session.query(Information).filter(Information.name == "Count frame").first()
            old_rsi = session.query(Information).filter(Information.name == "RSI").first()
            old_deposit = session.query(Information).filter(Information.name == "Deposit").first()

            first, twost, thirth, fourth, fiveth, sixth, seventh = (old_limit.data,
                                                           float(old_take_profit.data) * 100,
                                                           float(old_stop_lose.data) * 100,
                                                           old_time_frame.data,
                                                           old_count_frame.data,
                                                           old_rsi.data,
                                                           old_deposit.data)

            old_limit.data = data.get("limit")
            old_take_profit.data = float(data.get("take_profit")) * 0.01
            old_stop_lose.data = float(data.get("stop_lose")) * 0.01
            old_time_frame.data = data.get("time_frame")
            old_count_frame.data = data.get("count_frame")
            old_rsi.data = data.get("rsi")
            old_deposit.data = data.get("deposit")
            session.add(old_limit)
            session.add(old_deposit)
            session.add(old_time_frame)
            session.add(old_take_profit)
            session.add(old_stop_lose)
            session.add(old_rsi)
            session.add(old_count_frame)
            session.commit()
            await (callback_query.message if callback_query else message).answer(
                f"""
                
    ♻️Данные обновлены♻️
    
Лимит {first} -> {data.get("limit")}  
Take profit {round(twost, 2)}% -> {round(float(data.get("take_profit")), 2)}%📈
Stop lose {round(thirth, 2)}% -> % {round(float(data.get("stop_lose")), 2)}%📉
Time frame {fourth}📊 -> {data.get("time_frame")}📊
Count frame {fiveth}🕯-> {data.get("count_frame")}🕯
RSI {sixth} 🐃-> {data.get("rsi")}🐃
Deposit {seventh}💵 -> {data.get("deposit")} 💵 

/settings_now - 📁 Как нстроен бот
/start - 📋 Все команды 
                """,
            )

            await state.clear()  # Завершаем состояние

    except Exception as e:
        await state.clear()  # Завершаем состояние
        await message.reply(
            f"""
Произошла ошибка:  + {str(e)}

/start - 📋 Все команды 
""")




class Position:
    def __init__(self, symbol, volume, take_profit, stop_loss):
        self.symbol = symbol
        self.volume = volume
        self.take_profit = take_profit
        self.stop_loss = stop_loss
    def __repr__(self):
        return f"Position(symbol={self.symbol}, volume={self.volume}, take_profit={self.take_profit}, stop_loss={self.stop_loss})"


class TradingBot:
    def __init__(self):
        self.open_position = None

    def check_open_positions(self):
        return self.open_position is not None

    def close_all_positions(self):
        if self.open_position:
            symbol = self.open_position.symbol
            volume = self.open_position.volume

            try:
                side = 'SELL' if volume > 0 else 'BUY'

                order_response = client.new_order(symbol=symbol, side=side, type='MARKET', quantity=abs(volume))
                print(f"Закрыта позиция по {symbol} на {volume}.")
                send_message(f"Закрыта позиция по {symbol} на {volume}.")

                # Обнуляем открытую позицию
                self.open_position = None
            except Exception as e:
                print(f"Ошибка при закрытии позиции: {e}")
                send_message(f"Ошибка при закрытии позиции: {e}")

    @staticmethod
    def check_balance():
        # Получите текущий баланс пользователя
        balance_info = round(float(client.account()['availableBalance']), 1)
        return round(float(balance_info), 2)


    async def trade_logic(self):
        while is_running:
            if self.check_open_positions():
                send_message(f"""
                Есть открытая позиция!
                Монета: {self.open_position.symbol}
                Объем: {self.open_position.volume}
                Закрыть +: {self.open_position.take_profit}
                Закрыть -: {self.open_position.stop_loss}
                Цена сейчас: {get_symbol_price(self.open_position.symbol)}

                Закрыть позицию по текущей цене - /stop_all
                (Если позиция не закрылась лучше закрыть вручную на бирже)

                Следующая попытка через 5 минут...
                """)
                await asyncio.sleep(300)
                continue

            my_top_coins = get_top_coins()
            for symbol in my_top_coins:
                close = get_close_data(symbol)
                volume = get_trade_volume(symbol)
                rsi = calculate_rsi(close)
                ra = calculate_ra(close)
                price = get_symbol_price(symbol)
                c_f = session.query(Information).filter(Information.name == "Count frame").first().data
                period = int(session.query(Information).filter(Information.name == "Period").first().data)

                if len(close) >= period:
                    if rsi > int(session.query(Information).filter(Information.name == "RSI").first().data):
                        print(f"""
                            RSI монеты {symbol} оказался выше заданного значения {rsi}.
                            Это может привести к повышению риска!
                            (необходимо: {session.query(Information).filter(Information.name == "RSI").first().data})
                            Ищем дальше...
                            """)
                        await asyncio.sleep(5)
                        continue

                    if ra > price:
                            print(f"""
                                RA монеты {symbol} оказался больше цены токена в данный момент.
                                Это может привести к развороту рынка что не соответвует нашей стратегии.
                                RA {symbol}: {ra}$
                                Цена {symbol}: {price}$
                                Ищем дальше...
                                """)
                            await asyncio.sleep(5)
                            continue

                    if self.check_balance() < int(session.query(Information).filter(Information.name == "Deposit").data) * 3:
                        dep = session.query(Information).filter(Information.name == "Deposit").data
                        print(f"""
                            Недостаточно средств для открытия позиции по {symbol}.
                            Баланс: {self.check_balance()}
                            
                            Баланс должен превышать x3 указаный в настройках (сейчас: {dep})
                            """)
                        await asyncio.sleep(5)
                        continue

                    if close[-2] > close[-int(c_f) - 1]:

                        self.open_position = Position(symbol, volume, get_take_profit_price(price), get_stop_lose_price(price))
                        open_market_order(symbol, volume)
                        await asyncio.sleep(2)
                        open_stop_order(symbol, self.open_position.stop_loss, volume)
                        open_take_profit_order(symbol, self.open_position.take_profit, volume)
                        await asyncio.sleep(2)

                        send_message(f"""
                            ❕❕❕‼️‼️‼️‼️‼️‼️❕❕❕
                            Монета {symbol} соответствует нашим паттернам
                            
                            Цена монеты: {price}
                            Цена выхода +: {self.open_position.take_profit}
                            Цена выхода -: {self.open_position.stop_loss}
                            Период: {period}
                            RSI: {rsi}
                            RA: {ra}
                            """)

                        break  # Выход из цикла после открытия позиции

                else:
                    print("Данных для рассчета RSI и RA недостаточно")

            else:
                send_message("""Нет подходящих монет для торговли. Ожидание...100 секунд...""")
                await asyncio.sleep(100)

trading_bot = TradingBot()

async def main():
    create_datas()
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio

    Base.metadata.create_all(bind=engine)
    asyncio.run(main())