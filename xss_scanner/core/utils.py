import urllib.parse
import requests

def extract_params(url):
    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    return query_params

def inject_payloads(url, params, payloads):
    injected_urls = []
    for param in params:
        for payload in payloads:
            new_params = params.copy()
            new_params[param] = [payload]
            encoded_params = urllib.parse.urlencode(new_params, doseq=True)
            parsed = urllib.parse.urlparse(url)
            new_url = urllib.parse.urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                encoded_params,
                parsed.fragment
            ))
            injected_urls.append((param, payload, new_url))
    return injected_urls

def send_request(url, method="GET", headers=None, cookies=None, data=None):
    try:
        if method.upper() == "POST":
            response = requests.post(url, headers=headers, cookies=cookies, data=data, timeout=10, verify=False)
        else:
            response = requests.get(url, headers=headers, cookies=cookies, timeout=10, verify=False)
        return response
    except requests.RequestException as e:
        print(f"[!] Request to {url} failed: {e}")
        return None
