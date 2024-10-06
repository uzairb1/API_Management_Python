# Data Anonymization

## Overview

This project implements a comprehensive approach to anonymizing data using modern pipeline practices. The system is built to process and analyze data, ensuring quality and reliability through various checks. It is designed with Continuous Integration/Continuous Deployment (CI/CD) in mind, ensuring that the data quality checks and reports are automated, reliable, and efficient.

## Features

- **Data Quality Checks**: The system includes classes that perform various data quality checks, such as checking for missing values, validating email formats, and ensuring data consistency across various data types.
  
- **Automated Testing**: The project is equipped with unit tests that ensure the robustness of the data quality checks and other components. Tests are executed automatically using `pytest`, and logging is implemented to monitor both successes and failures.

- **Continuous Integration/Continuous Deployment (CI/CD)**: The project is structured to support CI/CD practices. The Docker container encapsulates all dependencies and configurations, allowing for seamless deployment and scaling.

- **Data Anonymization**: The system includes functionality for anonymizing sensitive data, which ensures compliance with data privacy regulations.

- **Logging and Monitoring**: The project employs logging mechanisms to track the execution of various components, making it easier to monitor system performance and troubleshoot issues.

## Project Structure

```plaintext
project-root/
├── data/                     # Directory for data storage (created at runtime)
├── queries/                  # SQL query files for report generation
├── src/                      # Source code directory
|   ├── queries/
|   |   ├── over_60_gmail.sql
|   |   ├── percentage_germany_email.sql
|   |   ├── top_three_gmail.sql
│   ├── __init__.py
│   ├── mask_list_faker.txt
│   ├── anonymize.py          # Script for data anonymization
│   ├── report.py             # Report generation based on SQL queries
│   ├── ingest.py             # Data ingestion scripts
├── tests/                    # Unit tests for the project
│   ├── __init__.py
│   ├── test_data_quality.py   # Tests for DataQuality class
│   ├── test_masked_data_quality.py  # Tests for MaskedDataQuality class
│   └── test_report.py        # Tests for ReportGenerator class
├── Dockerfile                 # Dockerfile for containerization
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
Requirements
Python 3.10 or higher
Docker
SQLite3
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/uzairb1/taxfix.git
cd yourproject
Build the Docker image:

bash
Copy code
docker build -t your_image_name .
Run the Docker container:

bash
Copy code
docker run -it -d your_container_name your_image_name
Running Tests
To execute the tests and verify that the data quality checks are functioning as expected, run:

bash
Copy code
docker run your_image_name pytest
This will execute the tests defined in the tests folder, logging the results in test_log.log.

To debug data in sqlite3 database create a new file within the src/queries folder with a .sql extension and write your query then copy the file into the container using
docker cp src/queries/your_file.sql your_container:/app/src/queries
then run the container again using
docker run -it -d your_container_name /bin/bash

Logging
The project logs key information and errors to test_log.log. You can check this file to see the results of the test runs, including which tests passed or failed.

Monitoring and Maintenance
To ensure continuous monitoring and maintenance of the system:

Monitor the test_log.log for errors or issues during the testing phase.
Regularly review the results of the data quality checks.
Adjust and enhance the quality checks and tests as needed based on the evolving data requirements.
