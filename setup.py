import time
from database import session, Information


def create_datas():
    from main import send_message
    if session.query(Information).first() is None:
        limit = Information(name="Лимит токенов", data=20)
        take = Information(name="Take profit", data=0.03)
        stop = Information(name="Stop lose", data=0.01)
        dep = Information(name="Deposit", data=1)
        tf = Information(name="Time Frame", data='15m')
        count_frame = Information(name="Count frame", data=2)
        period = Information(name="Period", data=7)
        rsi = Information(name="RSI", data=35)

        # Добавляем данные в сессию
        session.add(rsi)
        session.add(tf)
        session.add(period)
        session.add(count_frame)
        session.add(limit)
        session.add(take)
        session.add(stop)
        session.add(dep)
        session.commit()  # Коммитим изменения в базе данных
        send_message("""
Данные успешно созданы!

Лимит поиска токенов: 20
(Выберу топ 20 самых активных токенов и из найду точку входа)

Take profit: 3%
(Выйду из позиции если цена вырастет на 3%)

Stop lose: 1%
(Выйду из позиции если цена упадет на 1%)

Time frame: 15m
(15ти минутные свечи)

Count frame: 2
(Смотрю последние 2 свечи)

Период :7 дней
(RSI и RA смотрят метрику за последнюю неделю)



Deposit: 1$
(Вхожу в позицию на 1 usdt)

Бот начинает свою работу через 5 секунд!""")
        time.sleep(5)  # Ожидание 10 секунд
    else:
        print("Данные уже были созданы")

