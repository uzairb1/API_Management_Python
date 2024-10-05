import pandas as pd
import re
import sys
import os

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ingest import read_faker_api 

class DataQuality:
    def __init__(self, df):
        self.df = df
    def check_missing_values(self):
        """Check for missing values in the dataset."""
        missing_values = self.df.isnull().sum()
        return missing_values[missing_values > 0]

    def check_data_types(self):
        """Check if columns have the correct data types."""
        expected_types = {
            'firstname': 'object',
            'lastname': 'object',
            'email': 'object',
            'phone': 'object',
            'birthday': 'object',
            'country': 'object',
            'gender': 'object'
        }
        actual_types = self.df.dtypes
        return {col: (actual_types[col], expected_types[col]) for col in expected_types.keys() if col in self.df.columns and actual_types[col] != expected_types[col]}

    def check_email_format(self):
        """Check if email addresses are in valid format."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        invalid_emails = self.df[~self.df['email'].str.match(email_pattern)]
        if invalid_emails.empty:
            return "All Emails in correct format"
        else:
            return invalid_emails
        

    def validate_birthday_column(self, column_name='birthday'):
       
        if 'birthday' in self.df.columns:
            try:
                # Convert to datetime and validate the format
                valid_birthdays = pd.to_datetime(self.df['birthday'], format='%Y-%m-%d', errors='coerce')
                # Find invalid entries
                invalid_birthdays = self.df[valid_birthdays.isna()]
                return invalid_birthdays if not invalid_birthdays.empty else pd.DataFrame(columns=["birthday"])  # Return empty DataFrame
            except Exception as e:
                return pd.DataFrame(columns=["birthday"])  # Return empty DataFrame if an error occurs
        else:
            return pd.DataFrame(columns=["birthday"])  # Return empty DataFrame if column is missing


    def check_duplicates(self):
        """Check for duplicate records."""
        return self.df[self.df.duplicated()]

    def run_data_quality_checks(self):
        """Run all data quality checks and return results."""
        results = {
            'Missing Values': self.check_missing_values(),
            'Data Types': self.check_data_types(),
            'Invalid Emails': self.check_email_format(),
            'Duplicate Records': self.check_duplicates(),
            'Check Birthday Format':self.validate_birthday_column()
        }
        
        return results
