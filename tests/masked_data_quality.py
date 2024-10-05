import pandas as pd
import sqlite3

class MaskedDataQuality:
    def __init__(self, db_path, table_name, masked_columns):
        # Connect to the SQLite database
        self.conn = sqlite3.connect(db_path)
        # Read the specified table into a DataFrame
        self.df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
        self.masked_columns = masked_columns

    def check_masked_columns(self):
        """Check if the specified columns are masked with '****'."""
        masked_results = {}
        for column in self.masked_columns:
            if column in self.df.columns:
                masked_count = (self.df[column] == '****').sum()
                masked_results[column] = masked_count
            else:
                masked_results[column] = f"Column '{column}' does not exist in the DataFrame."
        
        # Return empty DataFrame if no masked columns found
        if all(count == 0 for count in masked_results.values() if isinstance(count, int)):
            return pd.DataFrame()  # Empty DataFrame
        return masked_results

    def check_birthday_column(self):
        """Check if the 'birthday' column contains only valid age ranges like '60-70'."""
        if 'birthday' in self.df.columns:
            # Regular expression to match valid age ranges (e.g., '60-70')
            valid_birthday_pattern = r'^\d{1,3}-\d{1,3}$'  
            # Find invalid entries that do not match the valid pattern
            invalid_birthday_entries = self.df[~self.df['birthday'].str.match(valid_birthday_pattern)]
            
            # Return empty DataFrame if no invalid entries found
            if invalid_birthday_entries.empty:
                return pd.DataFrame()  # Empty DataFrame
            return invalid_birthday_entries
        else:
            return "Column 'birthday' does not exist in the DataFrame."


    def check_email_column(self):
        """Check if the 'email' column contains only specific domains (gmail, hotmail, etc.)"""
        if 'email' in self.df.columns:
            # Updated pattern to check for specific domains
            domain_pattern = r'^([a-zA-Z0-9.-]+)$'  # e.g., gmail, hotmail, example
            invalid_email_entries = self.df[~self.df['email'].str.match(domain_pattern)]
            
            # Return empty DataFrame if no invalid entries found
            if invalid_email_entries.empty:
                return pd.DataFrame()  # Empty DataFrame
            return invalid_email_entries
        else:
            return "Column 'email' does not exist in the DataFrame."

    def run_all_checks(self):
        """Run all masked data quality checks and return results."""
        results = {
            'Masked Columns Check': self.check_masked_columns(),
            'Invalid Birthday Entries': self.check_birthday_column(),
            'Invalid Email Domains': self.check_email_column()
        }
        return results

    def close_connection(self):
        """Close the SQLite connection."""
        self.conn.close()


def read_masked_columns(path):
    """Reads the columns that are masked"""
    with open(path, 'r') as file:
        columns = file.read().strip().split(',')
    return [col.strip() for col in columns]
