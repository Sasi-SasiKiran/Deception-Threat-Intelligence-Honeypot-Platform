"""
Synthetic Attack Generator for Deception & Threat Intelligence Honeypot Platform.
Safely simulates realistic reconnaissance and brute force attacks against the decoy service.
"""

import time
import requests
import random
import argparse

ATTACK_PROFILES = [
    {
        "method": "POST",
        "path": "/wp-login.php",
        "data": {"log": "admin", "pwd": "Password123!", "wp-submit": "Log In"},
        "user_agent": "Mozilla/5.0 (Hydra-BruteForce/9.3)"
    },
    {
        "method": "POST",
        "path": "/wp-login.php",
        "data": {"log": "root", "pwd": "toor", "wp-submit": "Log In"},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) WPScan/3.8.22"
    },
    {
        "method": "GET",
        "path": "/wp-admin/",
        "data": None,
        "user_agent": "Mozilla/5.0 (compatible; ReconScanner/2.1)"
    },
    {
        "method": "GET",
        "path": "/robots.txt",
        "data": None,
        "user_agent": "Googlebot-Image/1.0 (Crawler)"
    },
    {
        "method": "GET",
        "path": "/.env",
        "data": None,
        "user_agent": "curl/8.1.2 (SecurityBot)"
    },
    {
        "method": "GET",
        "path": "/xmlrpc.php",
        "data": None,
        "user_agent": "python-requests/2.31.0"
    }
]

def run_simulation(target_url: str, count: int, delay: float):
    print(f"[*] Starting attack simulation targeting decoy at: {target_url}")
    print(f"[*] Dispatching {count} synthetic attacks with {delay}s delay...")

    success_intercepts = 0
    for i in range(1, count + 1):
        probe = random.choice(ATTACK_PROFILES)
        url = f"{target_url.rstrip('/')}{probe['path']}"
        headers = {
            "User-Agent": probe["user_agent"],
            "X-Forwarded-For": f"198.51.100.{random.randint(10, 240)}"
        }

        try:
            if probe["method"] == "POST":
                res = requests.post(url, data=probe["data"], headers=headers, timeout=5)
            else:
                res = requests.get(url, headers=headers, timeout=5)

            print(f"[{i}/{count}] {probe['method']} {probe['path']} -> HTTP {res.status_code} (Intercepted by Decoy)")
            success_intercepts += 1
        except Exception as e:
            print(f"[{i}/{count}] Error connecting to honeypot: {e}")

        if i < count:
            time.sleep(delay)

    print(f"\n[+] Simulation complete! {success_intercepts}/{count} events forwarded to pipeline.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Honeypot Synthetic Event Generator")
    parser.add_argument("--url", default="http://localhost:80", help="Decoy URL (default: http://localhost:80)")
    parser.add_argument("--count", type=int, default=8, help="Number of simulated attacks (default: 8 matching PDF validation)")
    parser.add_argument("--delay", type=float, default=0.8, help="Delay between attacks in seconds")
    args = parser.parse_args()

    run_simulation(args.url, args.count, args.delay)
