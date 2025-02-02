# Twitter Profile Scraper

This project is a Python script that uses Selenium to scrape profile details from Twitter. The script logs into Twitter, navigates to user profiles, and extracts information such as bio, location, website, following count, and followers count.

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
- Saves the scraped data into a CSV file.
- Uses **randomized delays** and **User-Agent rotation** to reduce detection risk.

## Requirements
Make sure you have the following installed:

- Python 3.x
- Google Chrome (or another compatible browser)
- Chrome WebDriver (compatible with your Chrome version)
- Required Python libraries:
  ```sh
  pip install selenium pandas
  ```

## Setup and Usage

1. **Download or Clone the Repository**
   ```sh
   git clone https://github.com/your-repo/twitter-scraper.git
   cd twitter-scraper
   ```

2. **Prepare Input CSV**
   - Create a CSV file (e.g., `twitter_links.csv`) with Twitter profile URLs in a single column.

3. **Set up WebDriver**
   - Download and place `chromedriver` in the system PATH or the project directory.

4. **Run the Script**
   - Replace the `username` and `password` variables in the script with your Twitter credentials.
   ```sh
   python twitter_scraper.py
   ```

5. **Output**
   - The script will create an output CSV file (`scraped_profiles_data.csv`) with the extracted details.

## Configuration Options
- The script runs in **headless mode** by default. You can disable it in `setup_driver()` by removing `options.add_argument("--headless")`.
- Adjust random delays between requests in `time.sleep(random.uniform(3, 7))` to reduce detection risk.
- Modify XPath selectors if Twitter changes its UI.

## Troubleshooting
- Ensure `chromedriver` is installed and matches your Chrome version.
- If login fails, check for additional verification steps (e.g., CAPTCHA, 2FA).
- If elements are not found, Twitter's UI may have changed; update the XPaths accordingly.

## Disclaimer
- Scraping Twitter data is subject to Twitter's [Terms of Service](https://twitter.com/en/tos).
- Use this script responsibly and only for ethical and legal purposes.

---

Happy scraping! 🚀

