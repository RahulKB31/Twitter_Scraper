---

# Twitter Profile Scraper with Database Integration

This project is a Python script that uses **Selenium** to scrape profile details from Twitter and store the data in a **MySQL database**. The script logs into Twitter, navigates to user profiles, extracts information such as bio, location, website, following count, and followers count, and stores the scraped data into a structured database table.

## Features
- Uses **Selenium WebDriver** for web automation.
- Logs into Twitter using credentials.
- Scrapes multiple profile pages from a CSV file.
- Extracts:
  - Bio
  - Location
  - Website
  - Following count
  - Followers count
- Stores the scraped data into a **MySQL database** (`twitter_db`) with a `profiles` table.
- Uses **randomized delays** and **User-Agent rotation** to reduce detection risk.
- Modular design with separate files for scraping, database operations, and utilities.

## Requirements
Make sure you have the following installed:
- Python 3.x
- Google Chrome (or another compatible browser)
- Chrome WebDriver (compatible with your Chrome version)
- Required Python libraries:
  ```sh
  pip install selenium pandas mysql-connector-python
  ```

## Setup and Usage

### 1. Download or Clone the Repository
```sh
git clone https://github.com/your-repo/twitter-scraper.git
cd twitter-scraper
```

### 2. Prepare Input CSV
- Create a CSV file (e.g., `twitter_links.csv`) with Twitter profile URLs in a single column. Example:
  ```
  https://twitter.com/user1
  https://twitter.com/user2
  https://twitter.com/user3
  ```

### 3. Set Up MySQL Database
- Install MySQL on your system if not already installed.
- Update the database credentials in `database.py`:
  ```python
  connection = mysql.connector.connect(
      host="localhost",       # Replace with your host
      user="root",            # Replace with your username
      password="password",    # Replace with your password
      database="twitter_db"   # Replace with your database name
  )
  ```

### 4. Set Up WebDriver
- Download the [ChromeDriver](https://sites.google.com/chromium.org/driver/) compatible with your Chrome version.
- Place `chromedriver` in the system PATH or the project directory.

### 5. Run the Script
- Replace the `username` and `password` variables in `scraper.py` with your Twitter credentials.
- Run the script:
  ```sh
  python main.py
  ```

### 6. Output
- The script will:
  - Drop and recreate the `twitter_db` database and `profiles` table if they exist.
  - Scrape data from the provided Twitter profile URLs.
  - Store the scraped data into the `profiles` table in the MySQL database.
- You can verify the data by querying the database:
  ```sql
  USE twitter_db;
  SELECT * FROM profiles;
  ```

## Configuration Options
- **Headless Mode**: The script runs in headless mode by default. To disable it, remove `options.add_argument("--headless")` in `utils.py`.
- **Random Delays**: Adjust random delays between requests in `time.sleep(random.uniform(3, 7))` to reduce detection risk.
- **XPath Selectors**: If Twitter changes its UI, update the XPath selectors in `scraper.py`.

## Project Structure
The project is modularized into separate files for better maintainability:
```
/twitter-scraper
    ├── main.py               # Main script to execute the program
    ├── scraper.py            # Functions for scraping Twitter profiles
    ├── database.py           # Functions for database setup and operations
    ├── utils.py              # Utility functions (e.g., WebDriver setup)
    ├── requirements.txt      # List of required Python libraries
    └── README.md             # Documentation for the project
    └── twitter_links.csv     # Links to scrape
    
```

## Troubleshooting
- **Ensure `chromedriver` is installed**: Make sure it matches your Chrome version.
- **Login Issues**: If login fails, check for CAPTCHA or two-factor authentication (2FA). This script does not handle 2FA.
- **Element Not Found**: If elements are not found, Twitter's UI may have changed; update the XPaths accordingly.
- **Database Errors**: Ensure MySQL is running and the credentials in `database.py` are correct.

## Disclaimer
- Scraping Twitter data is subject to Twitter's [Terms of Service](https://twitter.com/en/tos).
- Use this script responsibly and only for ethical and legal purposes.

---

Happy scraping and database integration! 🚀

---