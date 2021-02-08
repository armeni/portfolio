# Построение оптимизационного портфеля

### Задача
Построить оптимизационный портфель минимального риска из акций компаний индекса Доу-Джонса с использованием опционов. 

### Используемые библиотеки
- [numpy](https://numpy.org/), [scipy](https://www.scipy.org/): вычисления
- [pandas](https://pandas.pydata.org/): работа с данными
- [matplotlib](https://matplotlib.org/), [plotly](https://plotly.com/python/): визуализация
- [gurobipy](https://www.gurobi.com/): оптимизация
- [Alpha Vantage](https://www.alphavantage.co/documentation/): API для данных
- [requests](https://requests.readthedocs.io/en/master/): запросы к Alpha Vantage
- [Prophet](https://facebook.github.io/prophet/docs/quick_start.html#python-api): прогнозирование временных рядов

### Система файлов
- [reader.py](https://github.com/armeni/portfolio/blob/main/reader.py): чтение и предобработка даных. 
    * Класс GettingData с помощью requests обращается к сайту по тикеру компании и скачивает исторические данные (за 20+ лет) в формате csv. 
    * Класс Reader считывает csv-файл и обрабатывает его, оставляя только данные по дневным ценам закрытия торгов за определенный промежуток времени (с 03.01.2017 по 01.12.2020).

- [calculator.py](https://github.com/armeni/portfolio/blob/main/calculator.py): расчет необходимых значений для оптимизации (ожидаемая доходность портфеля, волатильность, риск порфтеля, стоимость опциона пут, ковариационная матрица).

- [forecast.ipynb](https://github.com/armeni/portfolio/blob/main/forecast.ipynb): прогнозирование цен акций компаний на месяц.

- [optimization.ipynb](https://github.com/armeni/portfolio/blob/main/optimization.ipynb): создание оптимизионной модели, вывод результатов.

- [results.csv](https://github.com/armeni/portfolio/blob/main/results.csv): все данные, включая прогноз. С этими данными происходит работа в optimization.ipynb
