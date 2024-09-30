import requests

class VirusTotal:
    def __init__(self,vt_token) -> None:
        self.vt_token = vt_token
    def query(self, params):
        url = ""
        if params['entity_type'].lower() == "hash":
            url = f"https://www.virustotal.com/api/v3/files/{params['entity']}"
        elif params['entity_type'].lower() == "url":
            url = f"https://www.virustotal.com/api/v3/urls/{params['entity']}"
        elif params['entity_type'].lower() == "ip":
            url = f"https://www.virustotal.com/api/v3/ip_addresses/{params['entity']}"
        elif params['entity_type'].lower() == "domain":
            url = f"https://www.virustotal.com/api/v3/domains/{params['entity']}"
        headers = {
            "x-apikey": self.vt_token
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error querying VirusTotal: {response.status_code}"}