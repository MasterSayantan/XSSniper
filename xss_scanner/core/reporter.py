import os
import json

def save_report(results, output_path):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
        print(f"[i] Report saved to: {output_path}")
    except Exception as e:
        print(f"[!] Failed to save report: {e}")
