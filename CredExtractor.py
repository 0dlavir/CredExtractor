import os
import re
import json
import csv
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm
import sys

# Configure logging
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

CREDENTIAL_PATTERN = re.compile(
    r'(https?://[^\s:/]+(?:\:\d+)?(?:/[^\s]*)?):([^:/\s]+):([^/\s]+)', re.IGNORECASE
)

def show_signature():
    signature = "\n".join([
        "╔════════════════════════════════════════╗",
        "║          Parsing Tools Extractor        ║",
        "║                Credentials              ║",
        "╚════════════════════════════════════════╝",
        "       Developed by Rivaldo Fendy Wijaya      "
    ])
    
    try:
        terminal_width = os.get_terminal_size().columns
        lines = signature.split('\n')
        centered_signature = "\n".join(line.center(terminal_width) for line in lines)
    except OSError:
        # Fallback if terminal size cannot be determined
        centered_signature = signature
    
    print(centered_signature)

def search_keywords_in_file(file_path: Path, keywords: List[str]) -> List[Dict[str, Any]]:
    search_results = []
    encodings_to_try = ['utf-8', 'ISO-8859-1', 'utf-16']
    
    for encoding in encodings_to_try:
        try:
            with file_path.open('r', encoding=encoding) as f:
                for line_number, line in enumerate(f, start=1):
                    match = CREDENTIAL_PATTERN.search(line)
                    if match:
                        url, username, password = match.groups()
                        if any(keyword.lower() in url.lower() for keyword in keywords):
                            search_results.append({
                                "url": url,
                                "username": username,
                                "password": password,
                                "source": str(file_path),
                                "line": line_number
                            })
            break  # Exit encoding loop if successful
        except UnicodeDecodeError:
            continue  # Try the next encoding
        except Exception as e:
            logging.error(f"Error reading {file_path} with encoding {encoding}: {e}")
            return [{"error": f"Error reading file with encoding {encoding}", "source": str(file_path)}]
    else:
        error_msg = f"Could not read {file_path} with available encodings"
        logging.error(error_msg)
        return [{"error": error_msg, "source": str(file_path)}]
    
    return search_results

def save_results(search_results: List[Dict[str, Any]], output_file: Path, output_format: str):
    try:
        if output_format == 'json':
            with output_file.open('w', encoding='utf-8') as f:
                json.dump(search_results, f, ensure_ascii=False, indent=4)
        elif output_format == 'csv':
            with output_file.open('w', newline='', encoding='utf-8') as f:
                fieldnames = ["url", "username", "password", "source", "line"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for result in search_results:
                    if "error" not in result:
                        writer.writerow(result)
        elif output_format == 'txt':
            with output_file.open('w', encoding='utf-8') as f:
                for result in search_results:
                    if "error" not in result:
                        f.write(
                            f"URL: {result['url']}, Username: {result['username']}, "
                            f"Password: {result['password']}, Source: {result['source']}, "
                            f"Line: {result['line']}\n"
                        )
        else:
            raise ValueError("Unsupported output format. Choose 'json', 'csv', or 'txt'.")
    except IOError as e:
        logging.error(f"IOError while saving results to {output_file}: {e}")
        print(f"An I/O error occurred while saving the results: {e}")
    except Exception as e:
        logging.error(f"Failed to save results to {output_file}: {e}")
        print(f"An error occurred while saving the results: {e}")

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search for credential patterns within text files."
    )
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help="Path to directory or specific file."
    )
    parser.add_argument(
        '--keywords',
        type=str,
        nargs='+',
        required=True,
        help="List of keywords to filter URLs."
    )
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help="Output file name (with extension .json, .csv, or .txt)."
    )
    return parser.parse_args()

def validate_output_path(output_path: Path):
    if output_path.exists():
        if output_path.is_dir():
            raise ValueError(f"The output path '{output_path}' is a directory.")
        else:
            # Prompt user for overwrite confirmation
            while True:
                response = input(f"The file '{output_path}' already exists. Overwrite? (y/n): ").strip().lower()
                if response == 'y':
                    break
                elif response == 'n':
                    print("Operation cancelled by the user.")
                    sys.exit(0)
                else:
                    print("Please respond with 'y' or 'n'.")
    else:
        # Ensure the parent directory exists
        parent = output_path.parent
        if not parent.exists():
            raise ValueError(f"The directory '{parent}' does not exist.")

def main():
    show_signature()
    args = parse_arguments()
    
    output_path = Path(args.output).resolve()
    try:
        validate_output_path(output_path)
    except ValueError as ve:
        logging.error(ve)
        print(f"Error: {ve}")
        sys.exit(1)
    
    output_format = output_path.suffix.lstrip('.').lower()
    
    if output_format not in {'json', 'csv', 'txt'}:
        print("Unsupported output format. Choose 'json', 'csv', or 'txt'.")
        sys.exit(1)
    
    path = Path(args.path).resolve()
    txt_files = []
    
    if path.is_file() and path.suffix == '.txt':
        txt_files.append(path)
    elif path.is_dir():
        txt_files.extend(path.rglob('*.txt'))
    else:
        print(f"The path '{args.path}' is neither a .txt file nor a directory.")
        sys.exit(1)
    
    if not txt_files:
        print("No .txt files found to process.")
        sys.exit(0)
    
    all_search_results = []
    
    with tqdm(total=len(txt_files), desc="Processing files", bar_format="{l_bar}{bar} | {percentage:3.0f}%") as progress_bar:
        for file_path in txt_files:
            results = search_keywords_in_file(file_path, args.keywords)
            all_search_results.extend(results)
            progress_bar.update(1)
    
    save_results(all_search_results, output_path, output_format)
    
    print(f"Search results have been saved to '{output_path}'")

if __name__ == '__main__':
    main()
