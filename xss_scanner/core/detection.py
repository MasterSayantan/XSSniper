import re
from .payloads import DOM_SINKS

def detect_reflected_xss(response_text, payload):
    # Check if payload appears in response text (case insensitive)
    if payload.lower() in response_text.lower():
        return True
    return False

def detect_dom_xss(response_text):
    # Scan for DOM sinks in the response text
    findings = []
    for sink in DOM_SINKS:
        pattern = re.compile(rf"{sink}", re.IGNORECASE)
        if pattern.search(response_text):
            findings.append(sink)
    return findings
