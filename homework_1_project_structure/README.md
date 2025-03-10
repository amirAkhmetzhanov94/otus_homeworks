# Log Analyzer

## Description
Log Analyzer is a Python-based tool designed to analyze log files, generate reports, and provide insights based on the log data. The tool supports both plain text and gzip-compressed log files.

## Project Structure


```plaintext
homework_1_project_structure/
├── Makefile
├── project/
│   ├── main.py
│   ├── config/
│   │   └── config.json
│   ├── data/
│   ├── src/
│   │   ├── app/
│   │   │   ├── log_file_helpers.py
│   │   │   ├── logger.py
│   │   │   ├── regex_helpers.py
│   │   │   └── report_helpers.py
│   ├── static/
│   └── tests/
│       ├── test_log_file_helpers.py
│       ├── test_logger.py
│       ├── test_regex_helpers.py
│       └── test_report_helpers.py
└── README.md
```


## Installation
To install the necessary dependencies and set up the environment, run:
```sh
make install
```

## Usage
To run the Log Analyzer with a specific configuration file, use:
```sh
make run
```

## Testing
To run the tests for the project, use:
```sh
make test
```

## Configuration
The configuration file (`config.json`) should be placed in the `project/config/` directory. It can override the default settings in the `main.py` file.

### Example `config.json`
```json
{
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "TEMPLATE_FILE": "report.html",
    "LOG_FILE": "app.log"
}
```
