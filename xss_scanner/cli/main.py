import sys
from xss_scanner.cli.cli import interactive_input, parse_args
from xss_scanner.core.payloads import load_payloads
from xss_scanner.core.utils import extract_params, inject_payloads, send_request
from xss_scanner.core.detection import detect_reflected_xss, detect_dom_xss
from xss_scanner.stored.stored_xss import check_stored_xss, discover_forms, submit_form
from xss_scanner.core.reporter import save_report

def main():
    if len(sys.argv) == 1:
        args_dict = interactive_input()
        # Convert dict to argparse.Namespace
        class Args:
            pass
        args = Args()
        for k, v in args_dict.items():
            setattr(args, k, v)
        # Set missing attributes to None or default
        if not hasattr(args, "stored_check_url"):
            args.stored_check_url = None
        if not hasattr(args, "header"):
            args.header = None
        if not hasattr(args, "only_reflected"):
            args.only_reflected = False
        if not hasattr(args, "silent"):
            args.silent = False
        if not hasattr(args, "stored"):
            args.stored = False
        if not hasattr(args, "render_url"):
            args.render_url = None
        if not hasattr(args, "output"):
            args.output = "results/xss.json"
        # Add color attributes to args for consistency
        args.color_red = getattr(args, "color_red", "\033[91m")
        args.color_blue = getattr(args, "color_blue", "\033[94m")
        args.color_yellow = getattr(args, "color_yellow", "\033[93m")
        args.color_reset = getattr(args, "color_reset", "\033[0m")
    else:
        args = parse_args()

    payloads = load_payloads(args.payload)
    params = extract_params(args.url)
    if not params:
        print("[!] No parameters found in the URL to test.")
        sys.exit(1)

    headers = {}
    if args.header:
        for h in args.header:
            if ":" in h:
                key, value = h.split(":", 1)
                headers[key.strip()] = value.strip()
    if args.cookie:
        headers["Cookie"] = args.cookie

    results = {
        "reflected_xss": [],
        "dom_xss": [],
        "stored_xss": []
    }

    injected_urls = inject_payloads(args.url, params, payloads)

    for param, payload, test_url in injected_urls:
        if not args.silent:
            print(f"[i] Testing parameter: {param} with payload: {payload}")
        response = send_request(test_url, method=args.method, headers=headers)
        if response and response.status_code == 200:
            if detect_reflected_xss(response.text, payload):
                result = {
                    "parameter": param,
                    "payload": payload,
                    "url": test_url,
                    "type": "reflected"
                }
                results["reflected_xss"].append(result)
                if not args.silent:
                    print(f"{args.color_red}[✓] Reflected XSS found in parameter: {param}{args.color_reset}")
                    print(f"{args.color_red}    Payload: {payload}{args.color_reset}")
                    print(f"{args.color_red}    URL: {test_url}{args.color_reset}")
            if not args.only_reflected:
                dom_findings = detect_dom_xss(response.text)
                if dom_findings:
                    result = {
                        "url": test_url,
                        "dom_sinks": dom_findings,
                        "type": "dom"
                    }
                    results["dom_xss"].append(result)
                    if not args.silent:
                        print(f"{args.color_blue}[!] DOM XSS detected via sinks: {', '.join(dom_findings)}{args.color_reset}")
                        print(f"{args.color_blue}    URL: {test_url}{args.color_reset}")

    # Stored XSS detection via stored-check-url
    if args.stored_check_url:
        stored_results = check_stored_xss(args.stored_check_url, payloads, headers, None)
        for res in stored_results:
            results["stored_xss"].append(res)
            if not args.silent:
                print(f"{args.color_yellow}[!] Stored XSS detected with payload: {res['payload']}{args.color_reset}")
                print(f"{args.color_yellow}    URL: {res['url']}{args.color_reset}")

    # Stored XSS detection via form injection
    if args.stored:
        if not args.silent:
            print("[+] Stored XSS Check enabled")
        forms = discover_forms(args.url, headers, None)
        for form in forms:
            stored_results = submit_form(form, args.url, payloads, headers, None)
            results["stored_xss"].extend(stored_results)
        # After submission, check render-url for stored payloads
        render_url = args.render_url if args.render_url else args.url
        stored_results = check_stored_xss(render_url, payloads, headers, None)
        for res in stored_results:
            if not args.silent:
                print(f"[!] Stored XSS Detected!")
                print(f"    - Form action: {res.get('form_action', 'N/A')}")
                print(f"    - URL: {res['url']}")
                print(f"    - Payload: {res['payload']}")
                print(f"    - Risk: HIGH")
            results["stored_xss"].append(res)

    if args.output:
        save_report(results, args.output)
