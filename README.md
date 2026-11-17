# OrangeHRM API Automation

## Project Overview

This project automates REST API testing for the OrangeHRM application using Python, Pytest, and Requests.

The framework covers positive and negative API scenarios for Employee and Recruitment Candidate APIs, including CRUD operations, validation, pagination, authentication, and end-to-end workflow testing.

## Technologies Used

- **Python 3.12**
- **Pytest** – Test execution and fixtures
- **Requests** – REST API automation
- **Allure** – Test reporting
- **PyCharm** – Development environment
- **Git/GitHub** – Version control

## Project Structure

```text
OrangeHRM_API_Automation/
│
├── utils/
│   └── loggers.py
│
├── Config.py
├── config.example.py
├── conftest.py
├── test_employee_api.py
├── README.md
└── .gitignore
```

### File Description

- **`test_employee_api.py`** – Contains the API test cases.
- **`conftest.py`** – Contains reusable Pytest fixtures, API client configuration, authentication, logging, and test-data cleanup.
- **`Config.py`** – Stores the local API configuration and Bearer token.
- **`config.example.py`** – Safe configuration template with a token placeholder.
- **`utils/loggers.py`** – Provides centralized logging.
- **`.gitignore`** – Prevents sensitive and generated files from being committed.
- **`README.md`** – Project documentation.


## API Test Coverage

The framework currently contains **15 automated test cases** covering the following scenarios:

### Employee APIs

- Get Employee Directory
- Verify Employee Data Type
- Get Employee by Valid ID
- Get Employee by Invalid ID
- Verify Invalid Token Handling
- Get Employee Directory with Limit
- Get Employee Directory with Limit and Offset
- Create Employee
- Create Employee Without Last Name
- Create Employee Without First Name

### Recruitment Candidate APIs

- Create Candidate
- Get Candidate
- Update Candidate
- Delete Candidate
- End-to-End Candidate CRUD Flow

### Testing Types Covered

- Positive testing
- Negative testing
- Data validation
- Authentication validation
- Pagination testing
- CRUD testing
- End-to-end workflow testing

## Configuration

1. Create a local `Config.py` file in the project root.
2. Add the OrangeHRM base URL and your Bearer token:

```python
BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php"
TOKEN = "YOUR_BEARER_TOKEN"
```

> **Note:** The actual `Config.py` containing the Bearer token should not be committed to GitHub. Use `config.example.py` as the safe configuration template.

## Install Dependencies

Activate the virtual environment and install the required packages:

```bash
pip install pytest requests allure-pytest
```

## Run Tests

Run all API tests using:

```bash
python -m pytest test_employee_api.py -v
```

The current test suite contains **15 tests**.

## Generate Allure Results

```bash
python -m pytest test_employee_api.py -v --alluredir=allure-results
```

## Open Allure Report

```bash
allure serve allure-results
```


## Framework Highlights

- Reusable API client using `requests.Session()`
- Bearer token authentication
- Pytest fixtures for reusable setup and test data
- Dynamic candidate ID generation
- Automatic cleanup of test data using fixture teardown
- Centralized API request and response logging
- Allure test titles and step-level reporting
- Positive and negative test scenarios
- Response status, schema, data type, and field-level assertions
- End-to-end Candidate CRUD validation
- Sensitive configuration excluded from version control