from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from main import *
import os

# Resolve the absolute path to the Frontend folder
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Frontend'))
print(f"Resolved Frontend path: {frontend_path}")

app = Flask(__name__, static_folder=frontend_path)

@app.route('/', methods=['GET'])
def home():
    # Serve index.html from the resolved Frontend folder path
    return send_from_directory(frontend_path, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    # Serve static files (CSS, JS, etc.) from the Frontend folder
    return send_from_directory(frontend_path, path)

# Endpoint to query forex data
@app.route('/api/forex-data', methods=['POST'])
def get_forex_data():
    from_currency = request.json.get('from')
    to_currency = request.json.get('to')
    period = request.json.get('period')
    date = period.split(" ")

    if not from_currency or not to_currency or not period:
        return jsonify({"error": "Missing required parameters"}), 400

    # Convert date strings to Unix timestamps
    from_date = get_unix_timestamp(date[0])
    to_date = get_unix_timestamp(date[1])

    # Create in-memory DB and get forex data
    conn, cursor = create_in_memory_db()

    # Fetch forex data from Yahoo
    data = fetch_forex_data(from_currency, to_currency, from_date, to_date)

    if data:
        # Save the fetched data into the database
        save_data_to_db(cursor, data)

        # Query the data from the in-memory database based on the period
        data = query_forex_data(cursor, from_currency, to_currency, period)
        return jsonify(data), 200
    else:
        return jsonify({"message": "No data found for the given period"}), 404


if __name__ == "__main__":
    app.run(debug=True)
