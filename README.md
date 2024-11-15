# CredExtractor

**CredExtractor** is a Python tool designed to search and extract credential patterns from text files. It scans specified directories or files for URLs containing usernames and passwords, filters them based on user-defined keywords, and exports the results in JSON, CSV, or TXT formats.

## Features

- **Pattern Matching:** Identifies credentials in the format `URL:username:password`.
- **Keyword Filtering:** Filters extracted URLs based on provided keywords.
- **Multiple Output Formats:** Export results as JSON, CSV, or TXT.
- **Progress Tracking:** Displays a progress bar during file processing.
- **Error Logging:** Logs errors to `error.log` for troubleshooting.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/0dlavir/CredExtractor.git
   cd CredExtractor

    Create a Virtual Environment (Optional but Recommended):

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies:

pip install -r requirements.txt

If requirements.txt is not provided, install the necessary packages manually:

    pip install tqdm

Usage

Run the CredExtractor.py script with the required arguments:

python CredExtractor.py --keywords <keyword1> <keyword2> ... --output <output_file> [--path <directory_or_file>]

Arguments

    --path: (Optional) Path to the target directory or specific .txt file. Defaults to the current directory (.).
    --keywords: (Required) One or more keywords to filter the URLs.
    --output: (Required) Name of the output file with extension .json, .csv, or .txt.

Examples

    Scan the Current Directory for Credentials with Specific Keywords and Output to JSON:

python CredExtractor.py --keywords example.com api --output results.json

Scan a Specific Directory and Output to CSV:

python CredExtractor.py --path /path/to/directory --keywords admin login --output creds.csv

Scan a Single File and Output to TXT:

    python CredExtractor.py --path /path/to/file.txt --keywords secure --output output.txt

Logging

Any errors encountered during execution are logged to error.log in the script's directory. Refer to this file for troubleshooting issues.
Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
License

This project is licensed under the MIT License.
Author

Rivaldo Fendy Wijaya

GitHub: 0dlavir