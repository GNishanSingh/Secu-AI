import requests

class VirusTotal:
    def __init__(self,vt_token) -> None:
        self.vt_token = vt_token
    def query(self, entity, entity_type):
        url = ""
        if entity_type == "hash":
            url = f"https://www.virustotal.com/api/v3/files/{entity[0]}"
        elif entity_type == "url":
            url = f"https://www.virustotal.com/api/v3/urls/{entity[0]}"
        elif entity_type == "ip":
            url = f"https://www.virustotal.com/api/v3/ip_addresses/{entity[0]}"
        headers = {
            "x-apikey": self.vt_token
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Return JSON data
        else:
            return {"error": f"Error querying VirusTotal: {response.status_code}"}