# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import pandas as pd

# List of User-Agent strings to randomize
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
]

# Function to set up WebDriver with a random user agent
def setup_driver():
    # Randomly select a user agent
    user_agent = random.choice(USER_AGENTS)
    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    return driver

# Function to check if already logged in
def is_logged_in(driver):
    try:
        # Navigate to the home page or profile page
        driver.get("https://twitter.com/home")
        time.sleep(7)  # Wait for the page to load
        # Check if the page title indicates you're logged in
        return "Home" in driver.title or "Twitter" in driver.title
    except Exception as e:
        print(f"Error checking login status: {e}")
        return False

# Function to log in to Twitter
def login_to_twitter(driver, username, password):
    try:
        # Open Twitter login page
        driver.get("https://twitter.com/login")
        time.sleep(3)  # Wait for the page to load

        # Enter username
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)  # Simulate pressing Enter instead of using submit()
        time.sleep(3)

        # Enter password
        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)  # Simulate pressing Enter instead of using submit()
        time.sleep(5)  # Wait for login to complete

        print("Logged in successfully!")
    except Exception as e:
        print(f"Error during login: {e}")

# Function to scrape profile details
def scrape_profile_details(driver, profile_url):
    try:
        # Navigate to the profile URL
        driver.get(profile_url)
        time.sleep(5)  # Wait for the page to load

        bio = "N/A"
        location = "N/A"
        website = "N/A"
        following_count = "N/A"
        followers_count = "N/A"

        # Extract Bio
        try:
            bio_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='UserDescription']"))
            )
            bio = bio_element.text.strip()
        except TimeoutException:
            pass

        # Extract Location
        try:
            location_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//span[@data-testid='UserLocation']//span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']"))
            )
            location = location_element.text.strip()
        except TimeoutException:
            pass

        # Extract Website
        try:
            website_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[@data-testid='UserUrl']"))
            )
            website = website_element.get_attribute("href")
        except TimeoutException:
            pass

        # Extract Following Count
        try:
            following_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "(//a[contains(@href, 'following')])[1]"))
            )
            following_count = following_element.text.strip(" Following")
        except TimeoutException:
            pass

        # Extract Followers Count
        try:
            followers_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "(//a[contains(@href, 'verified_followers')])[1]"))
            )
            followers_count = followers_element.text.strip(" Followers")
        except TimeoutException:
            pass

        # Return scraped data as a dictionary
        return {
            "Profile URL": profile_url,
            "Bio": bio,
            "Location": location,
            "Website": website,
            "Following Count": following_count,
            "Followers Count": followers_count
        }
    except Exception as e:
        print(f"Error scraping {profile_url}: {e}")
        return None

# Main function
def main():
    # Set up WebDriver with a random user agent
    driver = setup_driver()

    # Check if already logged in
    if not is_logged_in(driver):
        # Log in to Twitter
        username = "Rahul_AI"  # Replace with your Twitter username
        password = "123456789"  # Replace with your Twitter password
        login_to_twitter(driver, username, password)
    else:
        print("Already logged in!")

    # Read the input CSV file containing profile URLs
    input_csv = "twitter_links.csv"  # Replace with the actual filename
    output_csv = "scraped_profiles_data.csv"

    # Load the CSV file into a DataFrame
    try:
        df = pd.read_csv(input_csv, header=None)  # Treat the file as having no header
        profile_url_column = 0  # Assume the first column contains profile URLs
        print("Columns in the CSV file:", df.columns)  # Print column names for debugging
    except Exception as e:
        print(f"Error reading input CSV file: {e}")
        driver.quit()
        return

    # Scrape data for each profile URL
    scraped_data = []
    for index, row in df.iterrows():
        try:
            profile_url = row[profile_url_column]  # Use the dynamically determined column name
            if not profile_url or not profile_url.startswith("https://"):
                print(f"Skipping invalid URL in row {index + 1}: {profile_url}")
                continue
            print(f"Scraping {profile_url}...")
            profile_data = scrape_profile_details(driver, profile_url)
            if profile_data:
                scraped_data.append(profile_data)
            time.sleep(random.uniform(3, 7))  # Add a random delay to avoid detection
        except Exception as e:
            print(f"Error processing row {index + 1}: {e}")

    # Close the browser
    driver.quit()

    # Save the scraped data to a new CSV file
    if scraped_data:
        try:
            scraped_df = pd.DataFrame(scraped_data)
            scraped_df.to_csv(output_csv, index=False)
            print(f"Scraped data saved to {output_csv}")
        except Exception as e:
            print(f"Error saving scraped data to CSV: {e}")
    else:
        print("No data was scraped.")

# Run the script
if __name__ == "__main__":
    main()