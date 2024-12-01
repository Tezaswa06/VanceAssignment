import time
import sqlite3
from scrapper import fetch_exchange_data  
from time import sleep
from datetime import datetime, timedelta


conn = sqlite3.connect('forex_data.db')
cursor = conn.cursor()


currency_pairs = [
    ('GBP', 'INR'),
    ('AED', 'INR'),
    ('EUR', 'INR'),
    ('USD', 'INR'),
]


while True:
    for from_currency, to_currency in currency_pairs:
        
        table_name = f"exchange_rates_{from_currency}_{to_currency}"
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            adj REAL,
            volume INTEGER
        )
        ''')
        conn.commit()

        to_date = int(time.mktime(datetime.now().timetuple()))
        from_date = int(time.mktime((datetime.now() - timedelta(days=365)).timetuple())) #

        quote = f"{from_currency}{to_currency}=X"
        url = f"https://finance.yahoo.com/quote/{quote}/history/?period1={from_date}&period2={to_date}"
        exchange_data = fetch_exchange_data(url)

        if exchange_data is not None:
            
            exchange_data['Date'] = exchange_data['Date'].dt.strftime('%Y-%m-%d')

            #
            for index, row in exchange_data.iterrows():
                cursor.execute(f'''
                INSERT INTO {table_name} (date, open, high, low, close, adj, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (row['Date'], row.get('Open', None), row.get('High', None), row.get('Low', None),
                      row.get('Close', None), row.get('Adj', None), row.get('Volume', None)))
            conn.commit() 

    sleep(86400) 