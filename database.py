# Importing Necessary libraries
import mysql.connector

# Function to set up the database and create a table
def setup_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
        )

        cursor = connection.cursor()

        # Drop the table if it already exists
        cursor.execute("DROP DATABASE IF EXISTS twitter_db;")
        print("Existing 'database dropped!")

        # Create the database if it does not exist
        cursor.execute("CREATE DATABASE twitter_db;")
        print("New Database 'twitter_db' created!")

        # Switch to the newly created database
        connection.database = "twitter_db"

        # create a table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS profiles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            profile_url VARCHAR(255),
            bio TEXT,
            location VARCHAR(255),
            website VARCHAR(255),
            following_count VARCHAR(50),
            followers_count VARCHAR(50)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Database and table setup complete.")
        return connection, cursor
    except Exception as e:
        print(f"Error setting up database: {e}")
        return None, None

# Function to insert scraped data into the database
def insert_into_database(cursor, connection, profile_data):
    try:
        insert_query = """
        INSERT INTO profiles (profile_url, bio, location, website, following_count, followers_count)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        values = (
            profile_data["Profile URL"],
            profile_data["Bio"],
            profile_data["Location"],
            profile_data["Website"],
            profile_data["Following Count"],
            profile_data["Followers Count"]
        )
        cursor.execute(insert_query, values)
        connection.commit()
        print(f"Inserted data for {profile_data['Profile URL']} into the database.")
    except Exception as e:
        print(f"Error inserting data into database: {e}")

# Fetching all profiles
def fetch_all_profiles(cursor):
    try:
        cursor.execute("SELECT * FROM twitter_db.profiles;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error fetching data from database: {e}")































