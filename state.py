# import httpx
# from aiogram.filters import Command, StateFilter
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.storage.memory import MemoryStorage
#
# from main import bot, dp, types
# from database import Information, session, Orders, Base, engine
# from keyboard import get_limit_inline_keyboard, get_take_profit_keyboard, get_stop_lose_keyboard, get_time_frame_keyboard, get_count_frame_keyboard, get_deposit_keyboard
#
# storage = MemoryStorage()
#
# class Form(StatesGroup):
#     limit = State()
#     take_profit = State()
#     stop_lose = State()
#     time_frame = State()
#     count_frame = State()
#     deposit = State()
#
# @dp.message(Command("/settings"))
# async def start_feedback(message: types.Message, state: FSMContext):
#     try:
#         await state.set_state(Form.limit)  # Устанавливаем состояние для имени
#         await message.answer(f"""
# Бот фильтрует токены по активности и выбирает топ лучших
# Введите / выберите количество монет для поиска (сейчас {session.query(Information).filter(Information.name == "Лимит токенов").first().data}):
#         """,
#             reply_markup=get_limit_inline_keyboard(),
#         )
#     except Exception as e:
#         await message.answer("Произошла ошибка: " + str(e))  # Отладочная информация
#
# @dp.callback_query_handler(text="cancel", state=Form.limit)
# async def cancel_feedback(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message):
#     await state.clear()  # Завершаем состояние
#     await callback_query.answer("Изменение данных отменено!")  # Подтверждаем нажатие кнопки
#     await callback_query.message.answer(
#         """
# Бот останется со старыми данными.
# Старые данные - /settings_now
# Все команды - /start
#         """
#     )
#
# @dp.callback_query_handler(lambda c: c.data.startswith('limit_'), state=Form.limit)
# async def process_limit(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
#     try:
#         # Если callback_query передан, извлекаем лимит
#         if callback_query:
#             limit = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
#             await state.update_data(limit=limit)  # Сохраняем лимит в состоянии
#             await callback_query.answer()  # Подтверждаем нажатие кнопки
#         else:
#             # Если callback_query не передан, используем текст сообщения
#             limit = message.text
#             await state.update_data(limit=limit)  # Сохраняем лимит в состоянии
#
#         await state.set_state(Form.take_profit)  # Переходим к следующему состоянию
#         await (callback_query.message if callback_query else message).answer(
#             "Введите (число) / выберите процент роста при котором делать выход из позиции:",
#             reply_markup=get_take_profit_keyboard(),
#         )
#
#     except Exception as e:
#         await state.clear()  # Завершаем состояние
#         if callback_query:
#             await callback_query.message.answer(
#                 "Извините, наверное произошла какая-то неполадка, нужно попробовать немного позже.",
#             )
#         else:
#             await message.answer(
#                 "Извините, наверное произошла какая-то неполадка, нужно попробовать немного позже.",
#             )
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('profit_'), state=Form.take_profit)
# async def process_limit(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
#     try:
#         # Если callback_query передан, извлекаем лимит
#         if callback_query:
#             profit = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
#             await state.update_data(profit=profit)  # Сохраняем лимит в состоянии
#             await callback_query.answer()  # Подтверждаем нажатие кнопки
#         else:
#             # Если callback_query не передан, используем текст сообщения
#             profit = message.text
#             await state.update_data(profit=profit)  # Сохраняем лимит в состоянии
#
#         await state.set_state(Form.stop_lose)  # Переходим к следующему состоянию
#         await (callback_query.message if callback_query else message).answer(
#             "Введите (число) / выберите процент роста при котором делать выход из позиции:",
#             reply_markup=get_stop_lose_keyboard(),
#         )
#
#     except Exception as e:
#         await state.clear()  # Завершаем состояние
#         if callback_query:
#             await callback_query.message.answer(
#                 "Извините, наверное произошла какая-то неполадка, нужно попробовать немного позже.",
#             )
#         else:
#             await message.answer(
#                 "Извините, наверное произошла какая-то неполадка, нужно попробовать немного позже.",
#             )
#
# @dp.callback_query_handler(lambda c: c.data.startswith('stop_'), state=Form.stop_lose)
# async def process_limit(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
#     try:
#         # Если callback_query передан, извлекаем лимит
#         if callback_query:
#             stop = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
#             await state.update_data(stop=stop)  # Сохраняем лимит в состоянии
#             await callback_query.answer()  # Подтверждаем нажатие кнопки
#         else:
#             # Если callback_query не передан, используем текст сообщения
#             stop = message.text
#             await state.update_data(stop=stop)  # Сохраняем лимит в состоянии
#
#         await state.set_state(Form.time_frame)  # Переходим к следующему состоянию
#         await (callback_query.message if callback_query else message).answer(
#             "Введите (число) / выберите процент роста при котором делать выход из позиции:",
#             reply_markup=get_time_frame_keyboard(),
#         )
#
#     except Exception as e:
#         await state.clear()  # Завершаем состояние
#         if callback_query:
#             await callback_query.message.answer(
#                 "Извините, наверное произошла какая-то неполадка, нужно попробовать немного позже.",
#             )
#         else:
#             await message.answer(
#                 "Извините, наверное произошла какая-то неполадка, нужно попробовать немного позже.",
#             )
#
# @dp.callback_query_handler(lambda c: c.data.startswith('time_'), state=Form.time_frame)
# async def process_limit(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
#     try:
#         # Если callback_query передан, извлекаем лимит
#         if callback_query:
#             time = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
#             await state.update_data(time=time)  # Сохраняем лимит в состоянии
#             await callback_query.answer()  # Подтверждаем нажатие кнопки
#         else:
#             # Если callback_query не передан, используем текст сообщения
#             time = message.text
#             await state.update_data(time=time)  # Сохраняем лимит в состоянии
#
#         await state.set_state(Form.count_frame)  # Переходим к следующему состоянию
#         await (callback_query.message if callback_query else message).answer(
#             "Введите (число) / выберите процент роста при котором делать выход из позиции:",
#             reply_markup=get_count_frame_keyboard(),
#         )
#
#     except Exception as e:
#         await state.clear()  # Завершаем состояние
#         if callback_query:
#             await callback_query.message.answer(
#                 "Извините, наверное произошла какая-то неполадка, нужно попробовать немного позже.",
#             )
#         else:
#             await message.answer(
#                 "Извините, наверное произошла какая-то неполадка, нужно попробовать немного позже.",
#             )
#
# @dp.callback_query_handler(lambda c: c.data.startswith('count_'), state=Form.count_frame)
# async def process_limit(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
#     try:
#         # Если callback_query передан, извлекаем лимит
#         if callback_query:
#             count = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
#             await state.update_data(count=count)  # Сохраняем лимит в состоянии
#             await callback_query.answer()  # Подтверждаем нажатие кнопки
#         else:
#             # Если callback_query не передан, используем текст сообщения
#             count = message.text
#             await state.update_data(count=count)  # Сохраняем лимит в состоянии
#
#         await state.set_state(Form.deposit)  # Переходим к следующему состоянию
#         await (callback_query.message if callback_query else message).answer(
#             "Введите (число) / выберите процент роста при котором делать выход из позиции:",
#             reply_markup=get_deposit_keyboard(),
#         )
#
#     except Exception as e:
#         await state.clear()  # Завершаем состояние
#         if callback_query:
#             await callback_query.message.answer(
#                 "Извините, наверное произошла какая-то неполадка, нужно попробовать немного позже.",
#             )
#         else:
#             await message.answer(
#                 "Извините, наверное произошла какая-то неполадка, нужно попробовать немного позже.",
#             )
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('dep_'), state=Form.deposit)
# async def process_limit(callback_query: types.CallbackQuery, state: FSMContext, message: types.Message = None):
#     try:
#         # Если callback_query передан, извлекаем лимит
#         if callback_query:
#             dep = callback_query.data.split('_')[1]  # Извлекаем лимит из callback_data
#             await state.update_data(deposit=dep)  # Сохраняем лимит в состоянии
#             await callback_query.answer()  # Подтверждаем нажатие кнопки
#         else:
#             dep = message.text
#             await state.update_data(deposit=dep)  # Сохраняем лимит в состоянии
#
#         await state.set_state(Form.take_profit)  # Переходим к следующему состоянию
#
#         # Получаем все данные
#         data = await state.get_data()
#         old_limit = session.query(Information).filter(Information.name == "Лимит токенов").first().data
#         old_take_profit = session.query(Information).filter(Information.name == "Take profit").first().data
#         old_stop_lose = session.query(Information).filter(Information.name == "Stop lose").first().data
#         old_time_frame = session.query(Information).filter(Information.name == "Time Frame").first().data
#         old_count_frame = session.query(Information).filter(Information.name == "Count frame").first().data
#         old_deposit = session.query(Information).filter(Information.name == "Deposit").first().data
#
#         old_limit.data = data.get("limit")
#         old_take_profit.data = data.get("take_profit")
#         old_stop_lose.data = data.get("stop_lose")
#         old_time_frame.data = data.get("time_frame")
#         old_count_frame.data = data.get("count_frame")
#         old_deposit.data = data.get("deposit")
#
#         await (callback_query.message if callback_query else message).answer(
#             f"""
# Данные обновлены!
#
# Лимит {old_limit} -> {data.get("limit")}
# Take profit {old_take_profit}% -> {data.get("take_profit")}📈
# Stop lose {old_stop_lose}% -> % {data.get("stop_lose")}📉
# Time frame {old_time_frame}📊 -> {data.get("time_frame")}📊
# Count frame {old_count_frame}🔍-> {data.get("count_frame")}🔍
# Deposit {old_deposit}💵 -> {data.get("deposit")} 💵
#             """,
#         )
#
#         await state.clear()  # Завершаем состояние
#
#     except Exception:
#         await state.clear()  # Завершаем состояние
#         await message.answer(
#             "Извините, наверное произошла какая то неполадка, нужно попробовать немного позже.",
#         )
