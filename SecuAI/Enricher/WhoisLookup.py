from whois import whois

class WhoIsLookUp:
    def __init__(self) -> None:
        pass
    def query(self, params):
        reginfo = whois(params['domain'])
        try:
            return reginfo
        except:
            return "No registration information found"