# Forex Data Fetching and Querying API

This project provides a Flask-based API to fetch, store, and query Forex exchange rate data for multiple currency pairs. The data is fetched from Yahoo Finance, stored in an SQLite database, and can be queried through the API.

## Features

- Scrape Forex data for specific currency pairs from Yahoo Finance.
- Store the data in an SQLite database (in-memory or persistent).
- Query Forex data for specified date ranges via an API.
- Automate periodic data fetching and storage.

---

## File Structure

- `scraper.py` - Contains the logic for scraping Forex data from Yahoo Finance.
- `main.py` - Includes helper functions for database creation, timestamp conversion, and data querying.
- `app.py` - Flask application to expose an API endpoint for querying Forex data.
- `forex_data.db` - SQLite database (created dynamically) to store the Forex data.

---

## Prerequisites

- Python 3.8 or higher
- `pip` package manager

---

## Installation

1. **Clone the Repository**:
    ```bash
    git clone <your-repository-url>
    cd <repository-folder>
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Database**:
    - The database (`forex_data.db`) will be created dynamically by the script.

5. **To Run The App**:
    - To start the Flask web application, use the following command:

    ```bash
    python3 app.py
    ```

    - The terminal will show output indicating the server is running, typically:

    ```
    * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
    ```

    - Open your web browser and navigate to `http://127.0.0.1:5000` to access the Forex data querying API.

---

## Usage

### 1. **Running the Periodic Data Fetcher**

The `scraper.py` script periodically fetches and stores Forex data from
