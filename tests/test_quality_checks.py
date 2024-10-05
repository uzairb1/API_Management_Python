import pandas as pd
import sqlite3
import pytest
import logging
from tests.masked_data_quality import MaskedDataQuality, read_masked_columns 
from tests.data_quality_tests import DataQuality 
import sys
import os


sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ingest import read_faker_api 
from src.report import ReportGenerator

# Set up logging to file and console
log_file = "test_log.log"
logger = logging.getLogger(__name__)

# Add a FileHandler to write logs to a file
file_handler = logging.FileHandler(log_file, mode='a')
file_handler.setLevel(logging.INFO)

# Add a StreamHandler to also write logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Set up logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Set logging level
logger.setLevel(logging.INFO)

# Define a logger object
logger = logging.getLogger(__name__)

@pytest.fixture
def db_path():
    return "data/data.db"

@pytest.fixture
def masked_columns():
    path = "src/mask_list_faker.txt"
    return read_masked_columns(path)

@pytest.fixture
def queries_folder():
    return "src/queries/"

@pytest.fixture
def report_generator(db_path, queries_folder):
    return ReportGenerator(db_path, queries_folder)

def log_test_result(test_name, result):
    logger.info(f"Results for {test_name}:")
    if isinstance(result, pd.DataFrame) or isinstance(result, pd.Series):
        if not result.empty:
            logger.error(f"Issues found: \n{result}")
            pytest.fail(f"{test_name} failed with issues found.")
        else:
            logger.info("No issues found.")
    elif isinstance(result, dict):
        if result:
            logger.error(f"Issues found: \n{result}")
            pytest.fail(f"{test_name} failed with issues found.")
        else:
            logger.info("No issues found.")
    else:
        logger.info(result)
    for handler in logger.handlers:
            handler.flush()

# Test for DataQuality class
def test_data_quality(db_path):
   logger.info("Starting test: test_data_quality")
   try:
        df = read_faker_api(1000)

        # Initialize DataQuality class
        data_quality_checker = DataQuality(df)
        
        # Run the data quality checks
        results = data_quality_checker.run_data_quality_checks()
        
        # Log each test result
        for check, result in results.items():
            log_test_result(f"Data Quality Check - {check}", result)
            print(check)
            print(result)
   except Exception as e:
        logger.error(f"Exception occurred during data quality test: {str(e)}")
        pytest.fail(f"Test failed with exception: {str(e)}")

# Test for MaskedDataQuality class
def test_masked_data_quality(db_path, masked_columns):
    logger.info("Starting test: test_masked_data_quality")
    try:
        # Initialize MaskedDataQuality class
        masked_data_quality_checker = MaskedDataQuality(db_path, 'faker_data', masked_columns)
        
        # Run all checks
        results = masked_data_quality_checker.run_all_checks()
        
        # Log each test result
        for check, result in results.items():
            log_test_result(f"Masked Data Quality Check - {check}", result)

    except Exception as e:
        logger.error(f"Exception occurred during masked data quality test: {str(e)}")
        pytest.fail(f"Test failed with exception: {str(e)}")



# Test for ReportGenerator class
def test_generate_report(report_generator):
    logger.info("Starting test: test_generate_report")
    try:
        results_count = 0

        # Execute the report generation
        queries = report_generator.read_queries()

        for filename, query in queries.items():
            logger.info(f"Executing query: {filename}")
            result = report_generator.execute_query(query)
            
            if result:
                results_count += 1
                logger.info(f"Query {filename} returned results.")
            else:
                logger.error(f"No results returned for query: {filename}")
                pytest.fail(f"Query {filename} returned no results.")

        # Check if the correct number of results are returned (assuming there should be 3 queries)
        assert results_count == 3, f"Expected 3 results, but got {results_count}."
        logger.info("Report generation test passed with 3 results returned.")

    except Exception as e:
        logger.error(f"Exception occurred during report generation test: {str(e)}")
        pytest.fail(f"Test failed with exception: {str(e)}")