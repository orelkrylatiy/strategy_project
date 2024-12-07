import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Загрузка данных
df = pd.read_csv("ticks.csv", parse_dates=['Datetime'])
df['Datetime'] = pd.to_datetime(df['Datetime'])
df = df.sort_values('Datetime')


def build_time_bars(interval):
    #interval = '1min'
    # Построение тайм-баров с интервалом 1 минута
    time_bars = df.resample(interval, on='Datetime').agg({
        'price': ['first', 'last', 'max', 'min'],
        'volume': 'sum'
    })
    # Переименование колонок
    time_bars.columns = ['Open', 'Close', 'High', 'Low', 'Volume']
    # Удаление пустых строк, если в некоторые интервалы не попали данные
    time_bars = time_bars.dropna()

    return (time_bars)


def build_tick_bars(count_tick):
    # Добавление колонки 'tick' для кумулятивного подсчёта каждого тика
    df['tick'] = range(1, len(df) + 1)
    # Создание Tick bars: группировка каждых 100 тиков
    tick_bars = df.groupby((df['tick'] - 1) // count_tick).agg({
        'Datetime': 'first',
        'price': ['first', 'last', 'max', 'min'],
        'volume': 'sum'
    })

    # Переименование колонок для удобства
    tick_bars.columns = ['Open', 'Close', 'High', 'Low', 'Volume']

    # Вывод первых строк
    return (tick_bars)


def build_volume_bars(volume):
    volume = 1000
    df['cumulative_volume'] = df['volume'].cumsum()
    # Создаем группы на основе каждой тысячи кумулятивного объема
    df['volume_group'] = df['cumulative_volume'] // volume
    print(df)
    # Группировка по столбцу 'volume_bar' и вычисление объемных баров
    volume_bars = df.groupby('volume_group').agg({
        'Datetime': 'first',
        'price': ['first', 'last', 'max', 'min'],
        'volume': 'sum'
    })

    return (volume_bars)

def build_renko_bars(threshold):
    # Установка порога изменения цены
    threshold = 50
    # Вычисление изменений цены
    df['price_change'] = df['price'].diff().fillna(0).abs()
    # Инициализация
    group_number = 0
    df['group'] = 0
    cumulative_change = 0
    # Накопление изменений для группировки
    for index, row in df.iterrows():
        cumulative_change += row['price_change']
        if cumulative_change >= threshold:
            group_number += 1
            cumulative_change = 0
        df.at[index, 'group'] = group_number

    # Группировка и агрегирование
    price_bars = df.groupby('group').agg({
        'Datetime': 'first',
        'price': ['first', 'last', 'max', 'min'],
        'volume': 'sum'
    })

    # Переименование колонок
    price_bars.columns = ['Datetime', 'Open', 'Close', 'High', 'Low', 'Volume']

    return (price_bars)



# Предположим, что price_bars — это DataFrame с колонками 'Datetime', 'Open', 'Close', 'High', 'Low', 'Volume'
# Если у вас есть другой DataFrame, подставьте его название

def plot_bars(price_bars):
    # Устанавливаем фигуру и оси
    fig, ax = plt.subplots(figsize=(12, 6))

    # Форматирование временной оси
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    fig.autofmt_xdate()

    # Построение баров
    for index, row in price_bars.iterrows():
        color = 'green' if row['Close'] >= row['Open'] else 'red'
        # Линия High-Low
        ax.plot([row['Datetime'], row['Datetime']], [row['Low'], row['High']], color=color, linewidth=1)
        # Прямоугольник Open-Close
        ax.plot([row['Datetime'], row['Datetime']], [row['Open'], row['Close']], color=color, linewidth=3)

    # Настройки графика
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title('Renko Bars or Time Bars')

    plt.show()


price_bars = build_renko_bars(100)
price_bars = build_tick_bars(1000)
plot_bars(price_bars)
