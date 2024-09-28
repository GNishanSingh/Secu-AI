import requests

class URLScan:
    def __init__(self, urlscan_token) -> None:
        self.urlscan_token = urlscan_token
    def query(self, entity, entity_type):
        url = ""
        if entity_type == "url":
            url = f"https://urlscan.io/api/v1/search/?q=page.url:{entity}"
        elif entity_type == "domain":
            url = f"https://urlscan.io/api/v1/search/?q=domain:{entity}"
        elif entity_type == "ip":
            url = f"https://urlscan.io/api/v1/search/?q=ip:{entity}"
        elif entity_type == "hash":
            url = f"https://urlscan.io/api/v1/search/?q=hash:{entity}"
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
