import sys
import os

# Add current directory to sys.path to resolve module imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from xss_scanner.cli.main import main

if __name__ == "__main__":
    import requests
    # Disable warnings for insecure requests
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    main()
