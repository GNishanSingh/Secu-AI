import requests

class AlienVaultOTX:
    def __init__(self, otx_token) -> None:
        self.otx_token = otx_token
    def query(self, entity, entity_type):
        url = ""
        if entity_type == "hash":
            url = f"https://otx.alienvault.com/api/v1/indicators/file/{entity}/general"
        elif entity_type == "url":
            url = f"https://otx.alienvault.com/api/v1/indicators/url/{entity}/general"
        elif entity_type == "ip":
            url = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{entity}/general"
        elif entity_type == "domain":
            url = f"https://otx.alienvault.com/api/v1/indicators/domain/{entity}/general"
        
        headers = {
            "X-OTX-API-KEY": self.otx_token
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error querying AlienVault OTX: {response.status_code}"}
