import os
import sqlite3

class ReportGenerator:
    def __init__(self, db_name, queries_folder):
        self.db_name = db_name
        self.queries_folder = queries_folder

    def execute_query(self, query):
        """Executes a SQL query and returns the result."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            # Fetch column names
            column_names = [description[0] for description in cursor.description]
            print(column_names)
            # Print column names
            return results
        except sqlite3.Error as e:
            print(f"An error occurred while executing the query: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def read_queries(self):
        """Reads all SQL files from the queries folder."""
        queries = {}
        for filename in os.listdir(self.queries_folder):
            if filename.endswith('.sql'):
                file_path = os.path.join(self.queries_folder, filename)
                with open(file_path, 'r') as file:
                    query = file.read().strip()
                    queries[filename] = query
        return queries

    def generate_report(self):
        """Generates a report by executing all SQL queries and printing the results."""
        queries = self.read_queries()
        
        for filename, query in queries.items():
            print(f"Executing query from {filename}:")
            results = self.execute_query(query)
            if results is not None:
                for row in results:
                    print(row)
            print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    db_name = 'data/data.db'
    queries_folder = 'src/queries/'

    report_generator = ReportGenerator(db_name, queries_folder)
    report_generator.generate_report()
