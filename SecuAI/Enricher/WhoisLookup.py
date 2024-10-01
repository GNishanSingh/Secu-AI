import whois
import whois.whois

class WhoIsLookUp:
    def __init__(self) -> None:
        pass
    def query(self, domain):
        try:
            return whois.whois(domain)
        except:
            return "No registration information found"