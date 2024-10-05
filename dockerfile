# Use a Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the source code, tests, and requirements file into the container
COPY src/ src/
COPY tests/ tests/
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Create an empty folder for data that will be populated during the anonymization step
RUN mkdir data

# Run DataQuality tests first
# If the tests fail, the build will fail
RUN python -m pytest -k "test_data_quality" --log-cli-level=INFO --log-file=/app/test_log.log --log-file-level=INFO && \
    # If data quality tests pass, run the anonymize script
    python src/anonymize.py && \
    # Then, run masked data quality tests
    python -m pytest -k "test_masked_data_quality" --log-cli-level=INFO --log-file=/app/test_log.log --log-file-level=INFO && \
    # Finally, run report generation tests
    python -m pytest -k "test_generate_report" --log-cli-level=INFO --log-file=/app/test_log.log --log-file-level=INFO && \
    #run the report
    python src/report.py

# Default command (you can customize this, e.g., to run the application)
CMD ["python", "src/report.py"]
