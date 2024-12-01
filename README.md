# Forex Data Scraping and API Service

This repository contains the implementation of a Forex data scraping and API service project. The project covers all tasks and requirements as outlined in the assignment by Vance. The goal was to create a Flask-based API that fetches forex data from Yahoo Finance using Selenium and stores it in an in-memory SQLite database for efficient access.

## Features

- **Flask API**: A RESTful API built using Flask that handles the retrieval of forex data based on user inputs.
- **Selenium Web Scraping**: The script uses Selenium to scrape forex data from Yahoo Finance, ensuring dynamic content is fully loaded before data extraction.
- **In-Memory SQLite Database**: The scraped data is stored in an in-memory SQLite database, providing temporary and fast data storage for the application.
- **Error Handling & Debugging**: The project includes comprehensive error handling and debugging mechanisms to ensure smooth operation and facilitate troubleshooting.

## Installation

To run this project locally, you’ll need to have Python 3 and the required dependencies installed.

### Prerequisites

1. Python 3.x
2. Install required Python libraries:

   ```bash
   pip install -r requirements.txt
