import re
from mistralai import Mistral
import json
import cmd
import threading
import itertools
import time
import sys
import os
import colorama
from colorama import Fore, Style
from rich.console import Console
from rich.markdown import Markdown
import whois.whois
from SecuAI.Enricher.VirusTotal import VirusTotal
from SecuAI.Enricher.AlienVault import AlienVaultOTX
from SecuAI.Enricher.URLScan import URLScan
import whois
from dotenv import load_dotenv

load_dotenv()
colorama.init(autoreset=True)
class CybSecuAI:
    def __init__(self) -> None:
        self.VTLookup = VirusTotal(os.getenv('VirusTotal_Token'))
        self.AlienVault = AlienVaultOTX(os.getenv('AlienVault_OtxToken'))
        self.URLScan = URLScan(os.getenv('urlscan_token'))
    def MistralAgent (self, data):
        MistralToken = os.getenv("MistralToken")
        MistralAgent = os.getenv("MistralAgent")
        client = Mistral(api_key=MistralToken)
        chat_response = client.agents.complete(
            agent_id = MistralAgent,
            messages = [
                {
                    "role": "user",
                    "content": json.dumps(data),
                },
            ]
        )
        return chat_response.choices[0].message.content
    def use_nemo_for_decision(self, query):
        prompt = f"""
Check if User is requesting for any kind of API request. it might also contains IP, hash, domain, url, email, etc. extract what kind of API request user asking and provide answer only in following json format
{{
    'IsAPIRequest':true,
    'APIRequest':[
        {{
        'Type':'VirusTotal',
        'EntityType':'Hash',
        'Entities':['ffcad40333d105366b2037ab97e22c44']
        }}
        ]
}}

User Query: {query}
            
            """
        response = self.MistralAgent(prompt)
        try:
               return json.loads(response.replace('```json','').replace('```','').strip())
        except:
                return {'IsAPIRequest': False}
    def format_with_nemo(self, data, userquery):
        if "error" in data:
            return data["error"]
        else:
            prompt = f"""
    User asked for API data we got the data now user have query on that data. please complete user request.
    # API Data
    {data}
    # Question from user
    {userquery}
            """
            outputs = self.MistralAgent(prompt)
            return outputs
    def process_query(self, query):
        # entities = self.extract_entities(query)
        decs = self.use_nemo_for_decision(query)
        if decs['IsAPIRequest']:
                data = []
                for req in decs['APIRequest']:
                    if req['Type'] == 'VirusTotal':
                        for ioc in req['Entities']:
                            data.append(self.VTLookup.query(ioc, entity_type=req['EntityType'].lower()))
                    elif req['Type'] == 'WhoisLookup':
                        for ioc in req['Entities']:
                            data.append(whois.whois(ioc))
                    elif req['Type'] == 'AlienVault':
                        for ioc in req['Entities']:
                            data.append(self.AlienVault.query(ioc,req['EntityType'].lower()))
                    elif req['Type'] == 'URLScan':
                        for ioc in req['Entities']:
                            data.append(self.URLScan.query(ioc,req['EntityType'].lower()))
                    else:
                        data = "Lookup Not available Yet."
                return self.format_with_nemo(data, query)
        else:
            return self.MistralAgent(query)
    def spinner(self, stop_spinner):
        for cursor in itertools.cycle(['|', '/', '-', '\\']):
            if stop_spinner.is_set():
                break
            sys.stdout.write(f'\rAnalysing {cursor}')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\rDone!       \n')
        sys.stdout.flush()

    def process_query_with_spinner(self, query):
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(target=self.spinner, args=(stop_spinner,))
        spinner_thread.start()
        try:
            response = self.process_query(query)
        finally:
            spinner_thread.do_run = False
            stop_spinner.set()
            sys.stdout.flush()
            spinner_thread.join()
        return response

class CyberAssistantAI(cmd.Cmd):
    CySecuAIfn = CybSecuAI()
    os.system('cls')
    prompt = f"{Fore.GREEN}Secu-AI>{Style.RESET_ALL}"
    intro = f"{Fore.CYAN}Welcome to Gurmukh Cyber Assistant AI CLI! Type your query to get the help.{Style.RESET_ALL}"
    def __init__(self):
        super().__init__()
        self.console = Console()
    def default(self, query):
        response = self.CySecuAIfn.process_query_with_spinner(query)
        self.console.print(Markdown(response))
    def do_exit(self, arg):
        """Exit the CyberAssistant CLI."""
        print("Exiting the Secu-AI. Goodbye!")
        return True
    do_quit = do_exit
    do_EOF = do_exit
def main():
    CyberAssistantAI().cmdloop()
if __name__ == '__main__':
    main()

