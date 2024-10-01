import requests

class AlienVaultOTX:
    def __init__(self, otx_token) -> None:
        self.otx_token = otx_token
    def query(self, params):
        url = ""
        if params['entity_type'].lower() == "hash":
            url = f"https://otx.alienvault.com/api/v1/indicators/file/{params['entity']}/general"
        elif params['entity_type'].lower() == "url":
            url = f"https://otx.alienvault.com/api/v1/indicators/url/{params['entity']}/general"
        elif params['entity_type'].lower() == "ip":
            url = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{params['entity']}/general"
        elif params['entity_type'].lower() == "domain":
            url = f"https://otx.alienvault.com/api/v1/indicators/domain/{params['entity']}/general"
        
        headers = {
            "X-OTX-API-KEY": self.otx_token
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error querying AlienVault OTX: {response.status_code}"}
