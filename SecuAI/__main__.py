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
from SecuAI.Enricher.VirusTotal import VirusTotal
from dotenv import load_dotenv

load_dotenv()
colorama.init(autoreset=True)
class CybSecuAI:
    def __init__(self) -> None:
        self.VTLookup = VirusTotal(os.getenv('VirusTotal_Token'))
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

    def extract_entities(self, query):
        doc = query
        entities = {
            "ip_addresses": [],
            "hashes": [],
            "urls": []
        }
        hash_pattern =  re.findall(r"\b[0-9a-fA-F]{32,64}\b", doc)
        if hash_pattern:
            entities["hashes"].append(hash_pattern)
        return entities
    def use_nemo_for_decision(self, query, entities):
        if entities["hashes"] or entities["urls"] or entities["ip_addresses"]:
            prompt = f"""
            Does the following query require a VirusTotal API request?

            Query: {query}
            
            Answer 'yes' or 'no'.
            """
            response = self.MistralAgent(prompt)
            return "yes" in response.lower()
        else:
            return False
    def format_with_nemo(self, data, userquery, entity_type):
        if "error" in data:
            return data["error"]
        else:
            prompt = f"""
    User asked for virustotal data we got the data now user have query on that data. please complete user request.
    # Virustotal Data
    {data}
    # Question from user
    {userquery}
            """
            outputs = self.MistralAgent(prompt)
            return outputs
    def process_query(self, query):
        entities = self.extract_entities(query)
        if self.use_nemo_for_decision(query, entities):
            if entities["hashes"]:
                # Query VirusTotal with the hash
                vt_data = self.VTLookup.query(entities["hashes"][0], entity_type="hash")
                return self.format_with_nemo(vt_data, query, entity_type="hash")
            
            elif entities["urls"]:
                vt_data = self.VTLookup.query(entities["urls"][0], entity_type="url")
                return self.format_with_nemo(vt_data, entity_type="url")
            
            elif entities["ip_addresses"]:
                vt_data = self.VTLookup.query(entities["ip_addresses"][0], entity_type="ip")
                return self.format_with_nemo(vt_data, entity_type="ip")
        else:
            return "This query doesn't require a VirusTotal check. Please ask another question."
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
    prompt = f"{Fore.GREEN}CyberAssistantAI>{Style.RESET_ALL}"
    intro = f"{Fore.CYAN}Welcome to Gurmukh Cyber Assistant AI CLI! Type your query to get the help.{Style.RESET_ALL}"
    def __init__(self):
        super().__init__()
        self.console = Console()
    def default(self, query):
        response = self.CySecuAIfn.process_query_with_spinner(query)
        self.console.print(Markdown(response))
    def do_exit(self, arg):
        """Exit the CyberAssistant CLI."""
        print("Exiting the application. Goodbye!")
        return True
    do_quit = do_exit
    do_EOF = do_exit
def main():
    CyberAssistantAI().cmdloop()
if __name__ == '__main__':
    main()

