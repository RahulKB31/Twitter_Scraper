# Importing Necessary libraries
from scraper import scrape_profile_details, login_to_twitter, is_logged_in
from database import setup_database, insert_into_database, fetch_all_profiles
from utils import setup_driver
import pandas as pd
import time
import random

def main():
    # Set up Web Driver with a random user agent
    driver = setup_driver()

    # Check if already logged in
    if not is_logged_in(driver):
        # Log in to Twitter
        username = "Rahul_You******" # Use your username
        password = "******" # Use your password
        login_to_twitter(driver, username, password)
    else:
        print("Already logged in!")

    # Set up the databse
    connection, cursor = setup_database()
    if not connection or not cursor:
        print("Failed to connect to the database. Existing")
        driver.quit()
        return

    # Return the input CSV file containing URLs
    input_csv = "twitter_links.csv"
    try:
        df = pd.read_csv(input_csv, header=None) # Treat the file as having not header
        profile_url_column = 0 # The first column contains profile URLs
        print("Columns in the CSV file:", df.columns) # Print the column names for debugging
    except Exception as e:
        print(f"Error reading input CSV file: {e}")
        driver.quit()
        return

    # Scrape data for each profile URL
    for index, row in df.iterrows():
        try:
            profile_url = row[profile_url_column] # Use the dinamically determined column name
            if not profile_url or not profile_url.startswith("https://"):
                print(f"Skipping invalid URL in row {index + 1}: {profile_url}")
                continue
            print(f"Scrapping {profile_url}...")
            profile_data = scrape_profile_details(driver, profile_url)
            if profile_data:
                insert_into_database(cursor, connection, profile_data)
            time.sleep(random.uniform(3, 7)) # Add a random delay to avoid detection
        except Exception as e:
            print(f"Error processing row {index + 1}: {e}")

    # Fetch and display all profiles
    fetch_all_profiles(cursor)

    # Close the browser and database connection
    driver.quit()
    cursor.close()
    connection.close()
    print("Script Completed Successfully.")

if __name__ == "__main__":
    main()
