from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3
import time
from datetime import datetime


def build_yahoo_url(quote, from_date, to_date):
    return f"https://finance.yahoo.com/quote/{quote}/history/?period1={from_date}&period2={to_date}"


def get_unix_timestamp(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return int(time.mktime(dt.timetuple()))


def create_in_memory_db():
    conn = sqlite3.connect(":memory:")  
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forex_data (
            date TEXT,
            from_currency TEXT,
            to_currency TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            adj_close REAL,
            volume INTEGER
        )
    """)
    return conn, cursor


def save_data_to_db(cursor, data):
    for row in data:
        cursor.execute("""
            INSERT INTO forex_data (date, from_currency, to_currency, open, high, low, close, adj_close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (row['date'], row['from_currency'], row['to_currency'], row['open'], row['high'], row['low'], row['close'], row['adj_close'], row['volume']))


def fetch_forex_data(from_currency, to_currency, from_date, to_date):
    quote = f"{from_currency}{to_currency}%3DX"
    url = build_yahoo_url(quote, from_date, to_date)
    print(f"Scraping data from: {url}")

    
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    
    driver.get(url)

    
    wait = WebDriverWait(driver, 20)

    try:
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

       
        table = wait.until(EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "W(100%)")]')))
        rows = table.find_elements(By.TAG_NAME, 'tr')[1:] 
        data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) > 6:
                row_date = datetime.strptime(cols[0].text.strip(), "%b %d, %Y").strftime("%Y-%m-%d")
                data.append({
                    'date': row_date,
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'open': float(cols[1].text.strip().replace(',', '') or 0),
                    'high': float(cols[2].text.strip().replace(',', '') or 0),
                    'low': float(cols[3].text.strip().replace(',', '') or 0),
                    'close': float(cols[4].text.strip().replace(',', '') or 0),
                    'adj_close': float(cols[5].text.strip().replace(',', '') or 0),
                    'volume': int(cols[6].text.strip().replace(',', '') or 0)
                })
        return data
    except Exception as e:
        print(f"Error occurred: {e}")
        return []
    finally:
        driver.quit()


def query_forex_data(cursor, from_currency, to_currency, period):
   
    end_date = datetime.now()
    if period == "1W":
        start_date = end_date - timedelta(weeks=1)
    elif period == "1M":
        start_date = end_date - timedelta(days=30)
    elif period == "3M":
        start_date = end_date - timedelta(days=90)
    elif period == "6M":
        start_date = end_date - timedelta(days=180)
    elif period == "1Y":
        start_date = end_date - timedelta(days=365)
    else:
        return []

   
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    
    cursor.execute("""
        SELECT * FROM forex_data
        WHERE from_currency = ? AND to_currency = ? AND date BETWEEN ? AND ?
    """, (from_currency, to_currency, start_date_str, end_date_str))

    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append({
            'date': row[0],
            'from_currency': row[1],
            'to_currency': row[2],
            'open': row[3],
            'high': row[4],
            'low': row[5],
            'close': row[6],
            'adj_close': row[7],
            'volume': row[8]
        })
    return data
