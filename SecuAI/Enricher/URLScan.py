import requests

class URLScan:
    def __init__(self, urlscan_token) -> None:
        self.urlscan_token = urlscan_token
    def query(self, params):
        url = ""
        if params['entity_type'].lower() == "url":
            url = f"https://urlscan.io/api/v1/search/?q=page.url:{params['entity']}"
        elif params['entity_type'].lower() == "domain":
            url = f"https://urlscan.io/api/v1/search/?q=domain:{params['entity']}"
        elif params['entity_type'].lower() == "ip":
            url = f"https://urlscan.io/api/v1/search/?q=ip:{params['entity']}"
        elif params['entity_type'].lower() == "hash":
            url = f"https://urlscan.io/api/v1/search/?q=hash:{params['entity']}"
        else:
            return {"error": "Supported entity types are url, domain, ip, and hash."}
        headers = {
            "API-Key": self.urlscan_token
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()  # Return JSON data
        else:
            return {"error": f"Error querying URLScan: {response.status_code}"}
