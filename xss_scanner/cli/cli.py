import sys
import argparse

def interactive_input():
    # ANSI escape codes for RGBStrike colors
    RGBSTRIKE_GREEN = "\033[38;2;62;180;137m"
    RGBSTRIKE_RED = "\033[38;2;255;69;0m"
    RGBSTRIKE_BLUE = "\033[38;2;65;105;225m"
    RGBSTRIKE_YELLOW = "\033[38;2;255;215;0m"
    RESET_COLOR = "\033[0m"

    logo = f"""{RGBSTRIKE_BLUE}
             __  ______ ____        _                 
{RGBSTRIKE_RED}             \\ \\/ / ___/ ___| _ __ (_)_ __   ___ _ __ 
{RGBSTRIKE_BLUE}              \\  /\\___ \\___ \\| '_ \\| | '_ \\ / _ \\ '__|
{RGBSTRIKE_RED}              /  \\ ___) |__) | | | | | |_) |  __/ |   
{RGBSTRIKE_GREEN}             /_/\\_\\____/____/|_| |_|_| .__/ \\___|_|   
{RGBSTRIKE_RED}                                     |_|             
{RGBSTRIKE_BLUE}❖━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❖
{RGBSTRIKE_GREEN}✦  Created By       : Sayantan Saha                              ✦
{RGBSTRIKE_BLUE}✦  LinkedIn Profile : https://www.linkedin.com/in/mastersayantan ✦
{RGBSTRIKE_RED}✦  GitHub Profile   : https://github.com/MasterSayantan          ✦
{RGBSTRIKE_BLUE}❖━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❖
{RESET_COLOR}"""
    print(logo)
    print(f"{RGBSTRIKE_GREEN}Welcome to the XSS Vulnerability Scanner Tool{RESET_COLOR}")
    print(f"{RGBSTRIKE_GREEN}Please provide the following inputs:{RESET_COLOR}")
    url = input(f"{RGBSTRIKE_GREEN}🔗 URL (--url) [mandatory]: {RESET_COLOR}").strip()
    while not url:
        print(f"{RGBSTRIKE_GREEN}URL is mandatory.{RESET_COLOR}")
        url = input(f"{RGBSTRIKE_GREEN}🔗 URL (--url) [mandatory]: {RESET_COLOR}").strip()
    method = input(f"{RGBSTRIKE_GREEN}HTTP Method (--method) [GET/POST, default GET]: {RESET_COLOR}").strip().upper()
    if method not in ["GET", "POST"]:
        method = "GET"
    payload = input(f"{RGBSTRIKE_GREEN}💣 Payload file path (--payload) [optional]: {RESET_COLOR}").strip()
    # Validate payload file path if provided
    if payload:
        import os
        if not os.path.isfile(payload):
            print(f"{RGBSTRIKE_GREEN}[!] Payload file '{payload}' does not exist. Ignoring and using default payloads.{RESET_COLOR}")
            payload = None
    stored = input(f"{RGBSTRIKE_GREEN}🧪 Enable Stored XSS (--stored) [yes/no, default no]: {RESET_COLOR}").strip().lower()
    stored_flag = stored == "yes"
    only_reflected = input(f"{RGBSTRIKE_GREEN}🪞 Only Reflected XSS (--only-reflected) [yes/no, default no]: {RESET_COLOR}").strip().lower()
    only_reflected_flag = only_reflected == "yes"
    cookie = input(f"{RGBSTRIKE_GREEN}🍪 Cookie (--cookie) [optional]: {RESET_COLOR}").strip()
    render_url = input(f"{RGBSTRIKE_GREEN}👁️ Render URL (--render-url) [optional]: {RESET_COLOR}").strip()
    output = input(f"{RGBSTRIKE_GREEN}💾 Output file path (--output) [default results/xss.json]: {RESET_COLOR}").strip()
    if not output:
        output = "results/xss.json"
    silent = input(f"{RGBSTRIKE_GREEN}Silent mode (--silent) [yes/no, default no]: {RESET_COLOR}").strip().lower()
    silent_flag = silent == "yes"
    headers = []
    add_headers = input(f"{RGBSTRIKE_GREEN}Add additional headers? [yes/no]: {RESET_COLOR}").strip().lower()
    while add_headers == "yes":
        header = input(f"{RGBSTRIKE_GREEN}Header (format: HeaderName: value): {RESET_COLOR}").strip()
        if header:
            headers.append(header)
        add_headers = input(f"{RGBSTRIKE_GREEN}Add another header? [yes/no]: {RESET_COLOR}").strip().lower()
    return {
        "url": url,
        "method": method,
        "payload": payload if payload else None,
        "stored": stored_flag,
        "only_reflected": only_reflected_flag,
        "cookie": cookie if cookie else None,
        "render_url": render_url if render_url else None,
        "output": output,
        "silent": silent_flag,
        "header": headers if headers else None,
        "color_red": RGBSTRIKE_RED,
        "color_blue": RGBSTRIKE_BLUE,
        "color_yellow": RGBSTRIKE_YELLOW,
        "color_reset": RESET_COLOR
    }

def parse_args():
    class CustomHelpFormatter(argparse.HelpFormatter):
        def _format_action(self, action):
            help_text = super()._format_action(action)
            replacements = {
                '--url': '🔗 URL (--url): (mandatory)',
                '--payload': '💣 Payload (--payload): (optional, default payloads used if not provided)',
                '--stored': '🧪 Enable Stored XSS (--stored): (optional, default no)',
                '--only-reflected': '🪞 Only Reflected XSS (--only-reflected): (optional, default no)',
                '--cookie': '🍪 Cookie (--cookie): (optional)',
                '--render-url': '👁️ Render URL (--render-url): (optional)',
                '--output': '💾 Output (--output): (optional, default results/xss.json)'
            }
            for key, val in replacements.items():
                if key in help_text:
                    help_text = help_text.replace(key, val)
            return help_text

    parser = argparse.ArgumentParser(description="XSS Vulnerability Scanner Tool", formatter_class=CustomHelpFormatter)
    parser.add_argument("--url", required=True, help="Target URL to scan")
    parser.add_argument("--method", default="GET", choices=["GET", "POST"], help="HTTP method to use")
    parser.add_argument("--payload", help="Path to custom payload file")
    parser.add_argument("--cookie", help="Cookie header value")
    parser.add_argument("--header", action="append", help="Additional headers (can be used multiple times), format: HeaderName: value")
    parser.add_argument("--output", default="results/xss.json", help="Output file path to save report (JSON format)")
    parser.add_argument("--only-reflected", action="store_true", help="Only detect reflected XSS")
    parser.add_argument("--silent", action="store_true", help="Silent mode, minimal output")
    parser.add_argument("--stored-check-url", help="URL to check for stored XSS after injection")
    parser.add_argument("--stored", action="store_true", help="Enable stored XSS detection via form injection")
    parser.add_argument("--render-url", help="URL to check for stored payload after form submission")
    args = parser.parse_args()
    return args
