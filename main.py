import datetime as dt
# Неиспользуемый импорт.
import json
# Замечания по стилю кода:
# Проверьте пустые строки между классами, методами, функциями согласно https://www.python.org/dev/peps/pep-0008/#blank-lines
# Расставьте отступы вокруг арефметических знаков - например today_stats=0 -> today_stats = 0 или
# week_stats +=record.amount -> week_stats += record.amount
class Record:
    def __init__(self, amount, comment, date=''):
        self.amount=amount
        # Слишком сложное однострочное выражение, было бы более читаемо если бы вы переписали в несколько строк:
        # if not date:
        #     date = dt.datetime.now().date()
        #  self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.date = dt.datetime.now().date() if not date else dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment=comment
class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records=[]
    def add_record(self, record):
        self.records.append(record)
    def get_today_stats(self):
        today_stats=0
        # Обычные переменные не называются с заглавной буквы. Кроме того, здесь вы называете переменную
        # уже используемым именем, "затеняя" его в рамках вашего метода. Это означает, что ваша функция
        # перестала видеть класс Record, что может привести к ошибке в будущем, если вам понадобиться
        # использовать этот класс в функции. Старайтесь не использовать повторящиеся имена для ваших
        # функций, классов, переменных.
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats+Record.amount
        return today_stats
    def get_week_stats(self):
        week_stats=0
        # Очень часто вам необходимо получить текущую дату. Возможно было бы лучше создать функцию:
        # def get_today():
        #      return dt.datetime.now().date()
        # и использовать ее в Record.__init__, Calculator.get_today_stats, Calculator.get_week_stats и так далее.
        today = dt.datetime.now().date()
        for record in self.records:
            # Вы можете вынести число дней в переменную - days = (today -  record.date).days, это улучшит читаемость
            if (today -  record.date).days <7 and (today -  record.date).days >=0:
                week_stats +=record.amount
        return week_stats
class CaloriesCalculator(Calculator):
    # Для ревьюеров - по ТЗ метод должен называться get_calories_remained, что не отражает временных рамок метода,
    # в отличии от get_today_cash_remained. Если это сознательная задумка, то комментарий студента уместен, в
    # противном случае я бы предложил студенту переименовать метод и убрать комментарий.
    def get_calories_remained(self): # Получает остаток калорий на сегодня
        x=self.limit-self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал'
        # Этот else не нужен, можно просто выполнить return в конце функции.
        else:
            return 'Хватит есть!'
class CashCalculator(Calculator):
    # Ваш комментарий не нужен, так как вполне отражается именем переменной. Так же я бы рекомендовал 
    # использовать тип decimal.Decimal вместо float для денежных значений в будущем, подробнее можно почитать:
    # https://tirinox.ru/decimal-vs-float/
    USD_RATE=float(60) #Курс доллар США.
    EURO_RATE=float(70) #Курс Евро.
    # Возможно имеет смысл сделать рубли значением по умолчанию для currency.
    def get_today_cash_remained(self, currency, USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Эта переменная точно нужна? Вы бы могли обойтись без нее, используюя только currency.
        currency_type=currency
        cash_remained = self.limit - self.get_today_stats()
        if currency=='usd':
            cash_remained /= USD_RATE
            currency_type ='USD'
        elif currency_type=='eur':
            cash_remained /= EURO_RATE
            currency_type ='Euro'
        elif currency_type=='rub':
            # У вас здесь опечатка, которая приводит к багу. Стоит добавить сценарии тестирования как описано в
            # рекомендациях, чтобы избежать таких ошибок.
            cash_remained == 1.00
            currency_type ='руб'
        # Стоит добавить обработку ошибок для некорректных типов валют.
        if cash_remained > 0:
            # Согласно требованиям к коду в f-строках недопустимы математические операции
            # https://docs.google.com/document/d/1s_FqVkqOASwXK0DkOJZj5RzOm4iWBO5voc_8kenxXbw/edit
            return f'На сегодня осталось {round(cash_remained, 2)} {currency_type}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Этот elif не нужен, так как уже известно, что cash_remained не равен 0, и не больше 0.
        elif cash_remained < 0:
            return 'Денег нет, держись: твой долг - {0:.2f} {1}'.format(-cash_remained, currency_type)
    # Нет необходимости объявлять этот метод, так как если метод не объявлен у наследника, то он автоматически
    # используется из родительского класса. Подробнее: https://tirinox.ru/mro-python/
    def get_week_stats(self):
        super().get_week_stats()
