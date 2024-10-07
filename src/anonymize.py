import pandas as pd
import sqlite3
import os
from datetime import datetime
from ingest import read_faker_api

class AnonymizeData:
    def __init__(self, db_name, table_name, mask_file):
        self.db_name = db_name
        self.table_name = table_name
        self.mask_file = mask_file
        self.df = None
    
    def read_columns_to_be_masked(self):
        """Reads the columns to be masked from a specified file."""
        with open(self.mask_file, 'r') as file:
            columns = file.read().strip().split(',')
        return [col.strip() for col in columns]

    def load_data(self, quantity):
        """Loads data from the Faker API."""
        self.df = read_faker_api(quantity)
    
    def anonymize_birthday(self):
        """Anonymizes the 'birthday' column by converting it to age groups."""
        current_year = datetime.now().year
        self.df['birth_year'] = self.df['birthday'].str[:4].astype(int)
        age_group_start = ((current_year - self.df['birth_year']) // 10 * 10).astype(str)
        age_group_end = (age_group_start.astype(int) + 10).astype(str)
        self.df['birthday'] = age_group_start + '-' + age_group_end
        self.df.drop(columns=['birth_year'], inplace=True)
    
    def anonymize_email(self):
        """Anonymizes the 'email' column by keeping only the domain name."""
        self.df['email'] = self.df['email'].str.split('@').str[1].str.split('.').str[0]

    def mask_columns(self, columns):
        """Masks specified columns in the DataFrame with '****'."""
        for column in columns:
            if column in self.df.columns:
                self.df[column] = '****'
            else:
                print(f"Column '{column}' does not exist in the DataFrame.")

    def store_in_sqlite(self):
        """Stores the DataFrame in an SQLite database."""
        try:
            # Check if the database file exists
            if not os.path.exists(self.db_name):
                print(f"{self.db_name} does not exist. Creating a new database.")

            # Connect to SQLite database
            with sqlite3.connect(self.db_name) as conn:
                print(f"Connected to database: {self.db_name}")

                # Store the DataFrame in the specified table
                self.df.to_sql(self.table_name, conn, if_exists='append', index=False)
                print(f"DataFrame stored in table '{self.table_name}' successfully.")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    
    def read_from_sqlite(self):
        """Reads a DataFrame from the SQLite database."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            print(f"Connected to database: {self.db_name}")
            df = pd.read_sql_query(f"SELECT * FROM {self.table_name}", conn)
            return df
        except sqlite3.Error as e:
            print(f"An error occurred while reading the database: {e}")
        finally:
            if conn:
                conn.close()
                print("Connection closed.")


    def run(self, quantity):
        """Executes the full anonymization and storage process."""
        # Load columns to mask
        anon_cols = self.read_columns_to_be_masked()
        
        # Load data
        self.load_data(quantity)

        # Anonymize data
        self.anonymize_birthday()
        self.anonymize_email()
        self.mask_columns(anon_cols)

        # Store the anonymized DataFrame in the SQLite database
        self.store_in_sqlite()

        # Read the stored DataFrame back for verification
        new_df = self.read_from_sqlite()
        print("Retrieved DataFrame from SQLite database:")
        print(new_df)


if __name__ == "__main__":
    file_path = 'src/mask_list_faker.txt'
    db_name = 'data/data.db'
    table_name = 'faker_data'
    quantity = 1000

    anonymizer = AnonymizeData(db_name, table_name, file_path)
    #function should be run 30 times for prod deployment
    #for i in range(30):
     #   anonymizer.run(quantity)
    anonymizer.run(quantity)
