# XSSniper (XSS Vulnerability Scanner Tool)

## Overview
This tool is designed to scan web applications for Cross-Site Scripting (XSS) vulnerabilities, including reflected, stored, and DOM-based XSS. It supports both GET and POST HTTP methods, custom payloads, and advanced features like form discovery and submission for stored XSS detection.

## Features
- **Reflected XSS Detection:** Injects payloads into URL parameters and checks for reflections in the response.
- **Stored XSS Detection:** Supports detection via stored-check URLs and form injection.
- **DOM XSS Detection:** Scans response content for common DOM sink patterns.
- **Custom Payloads:** Allows users to specify a file with custom payloads.
- **HTTP Methods:** Supports GET and POST requests.
- **Headers and Cookies:** Supports additional HTTP headers and cookie injection.
- **Interactive Mode:** Provides a user-friendly interactive input mode.
- **JSON Reporting:** Saves scan results in JSON format for easy analysis.
- **Form Discovery and Submission:** Automatically discovers forms on pages and submits payloads for stored XSS testing.

## Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Steps
1. Clone or download the repository.
2. Navigate to the project directory.
3. Install required dependencies:

```bash
git clone https://github.com/MasterSayantan/XSSniper.git
cd XSSniper
pip install -r requirements.txt
```

## Usage

### Interactive Mode
Run the script without arguments to enter interactive mode:

```bash
python3 XSSniper.py
```

You will be prompted to enter the target URL, HTTP method, payload file path, and other options.

### Command Line Arguments
Run the script with command line arguments for automation:

```bash
python3 XSSniper.py --url "http://example.com/page?param=value" --method GET --payload payloads.txt --stored --output results/xss_report.json
```

### Key Arguments
- `--url`: Target URL to scan (mandatory)
- `--method`: HTTP method (GET or POST, default GET)
- `--payload`: Path to custom payload file (optional)
- `--stored`: Enable stored XSS detection via form injection (optional)
- `--only-reflected`: Detect only reflected XSS (optional)
- `--cookie`: Cookie header value (optional)
- `--header`: Additional headers (can be used multiple times)
- `--output`: Output file path for JSON report (default: results/xss.json)

## Author
- **Sayantan Saha**
- LinkedIn: [https://www.linkedin.com/in/mastersayantan](https://www.linkedin.com/in/mastersayantan)
- GitHub: [https://github.com/MasterSayantan](https://github.com/MasterSayantan)


