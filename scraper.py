# Importing Necessary libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

# Function to check if already logged in
def is_logged_in(driver):
    try:
        driver.get("https://twitter.com/home")
        time.sleep(7) # Wait for the page to load
        return "Home" in driver.title or "Twitter" in driver.title
    except Exception as e:
        print(f"Error checking login status: {e}")
        return False

# Function to log in to Twitter
def login_to_twitter(driver, username, password):
    try:
        driver.get("https://twitter.com/home")
        time.sleep(3)
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)
        time.sleep(3)
        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)
        print("Logged in Successfully!")
    except Exception as e:
        print(f"Error during login: {e}")

# Function to scrape profile details
def scrape_profile_details(driver, profile_url):
    try:
        driver.get(profile_url)
        time.sleep(5)
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

        return {
            "Profile URL": profile_url,
            "Bio": bio,
            "Location": location,
            "Website": website,
            "Following Count": following_count,
            "Followers Count": followers_count
        }
    except Exception as e:
        print(f"Error scrapping {profile_url}: {e}")
        return None
















