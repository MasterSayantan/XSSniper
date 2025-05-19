import requests
import urllib.parse

def check_stored_xss(stored_url, payloads, headers, cookies):
    stored_results = []
    try:
        response = requests.get(stored_url, headers=headers, cookies=cookies, timeout=10, verify=False)
        if response.status_code == 200:
            for payload in payloads:
                if payload.lower() in response.text.lower():
                    stored_results.append({
                        "url": stored_url,
                        "payload": payload,
                        "type": "stored"
                    })
        return stored_results
    except requests.RequestException as e:
        print(f"[!] Stored XSS check request failed: {e}")
        return []

def discover_forms(url, headers, cookies):
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10, verify=False)
        if response.status_code != 200:
            return []
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        forms = []
        for form in soup.find_all("form"):
            form_details = {}
            form_details["action"] = form.get("action")
            form_details["method"] = form.get("method", "get").lower()
            inputs = []
            for input_tag in form.find_all("input"):
                input_type = input_tag.get("type", "text")
                input_name = input_tag.get("name")
                if input_name:
                    inputs.append({"type": input_type, "name": input_name})
            form_details["inputs"] = inputs
            forms.append(form_details)
        return forms
    except Exception as e:
        print(f"[!] Failed to discover forms: {e}")
        return []

def submit_form(form, base_url, payloads, headers, cookies):
    stored_results = []
    for payload in payloads:
        data = {}
        for input_field in form["inputs"]:
            # Inject payload into all input fields
            data[input_field["name"]] = payload
        action = form["action"]
        if not action or action == "":
            action = base_url
        else:
            action = urllib.parse.urljoin(base_url, action)
        method = form["method"]
        try:
            if method == "post":
                response = requests.post(action, data=data, headers=headers, cookies=cookies, timeout=10, verify=False)
            else:
                response = requests.get(action, params=data, headers=headers, cookies=cookies, timeout=10, verify=False)
            if response.status_code == 200:
                stored_results.append({
                    "form_action": action,
                    "payload": payload,
                    "type": "stored"
                })
                print(f"[+] Form action found: {action}")
                print(f"[✓] Injected and submitted payload: {payload}")
        except requests.RequestException as e:
            print(f"[!] Form submission failed: {e}")
    return stored_results
