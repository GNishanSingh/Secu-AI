from mistralai import Mistral
import json
import cmd
import sys
import os
import colorama
from colorama import Fore, Style
from rich.console import Console
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import SpinnerColumn, Progress
from dotenv import load_dotenv
from SecuAI.SimilarityModule import IsAPIRequest
from SecuAI.toolsAI import MistralToolAI
import importlib.metadata

load_dotenv()
colorama.init(autoreset=True)
class CybSecuAI:
    def __init__(self) -> None:
        MistralToken = os.getenv("MistralToken")
        self.MistralAgentstring = os.getenv("MistralAgent")
        self.client = Mistral(api_key=MistralToken)
        self.tools = MistralToolAI(self.client)
        self.checkrequest = IsAPIRequest()
    def MistralAgent (self, data):
        chat_response = self.client.agents.complete(
            agent_id = self.MistralAgentstring,
            messages = [
                {
                    "role": "user",
                    "content": json.dumps(data,default=str),
                },
            ]
        )
        return chat_response.choices[0].message.content
    def process_query(self, query):
        decs = self.checkrequest.check(query)
        if decs:
            return self.tools.getfunctiondetails(query)
        else:
            return self.MistralAgent(query)
    def process_query_with_spinner(self, query):
        with Progress(SpinnerColumn(),transient=True,) as progress:
            task = progress.add_task("[cyan]Analyzing...",total=None)
            try:
                response = self.process_query(query)
            finally:
                sys.stdout.flush()
            progress.stop_task(task)
        return response
class CyberAssistantAI(cmd.Cmd):
    CySecuAIfn = CybSecuAI()
    pkgmeta = importlib.metadata.metadata("SecuAI")
    os.system('cls')
    prompt = f"{Fore.GREEN}Secu-AI>{Style.RESET_ALL}"
    intro = f"""
{Fore.CYAN}

███████╗███████╗ ██████╗██╗   ██╗       █████╗ ██╗
██╔════╝██╔════╝██╔════╝██║   ██║      ██╔══██╗██║
███████╗█████╗  ██║     ██║   ██║█████╗███████║██║
╚════██║██╔══╝  ██║     ██║   ██║╚════╝██╔══██║██║
███████║███████╗╚██████╗╚██████╔╝      ██║  ██║██║
╚══════╝╚══════╝ ╚═════╝ ╚═════╝       ╚═╝  ╚═╝╚═╝
{Style.RESET_ALL}
{Fore.BLUE}Version{Style.RESET_ALL}         : {'v'+pkgmeta['version']}
{Fore.BLUE}Description{Style.RESET_ALL}     : {pkgmeta['summary']}
{Fore.BLUE}Author{Style.RESET_ALL}          : {pkgmeta['author']}
{Fore.BLUE}Email{Style.RESET_ALL}           : {pkgmeta['author-email']}
{Fore.BLUE}Documentation{Style.RESET_ALL}   : {pkgmeta['Home-page']}
{Fore.BLUE}Requirements{Style.RESET_ALL}    : {f"{Fore.GREEN}✔{Style.RESET_ALL}  Mistral AI Token" if os.getenv('MistralAgent') is not None else f"{Fore.RED}❌{Style.RESET_ALL} Mistral AI Token"}
                : {f"{Fore.GREEN}✔{Style.RESET_ALL}  VirusTotal Token" if os.getenv('VirusTotal_Token') is not None else f"{Fore.RED}❌{Style.RESET_ALL} VirusTotal Token"}
                : {f"{Fore.GREEN}✔{Style.RESET_ALL}  AlienVault Token" if os.getenv('AlienVault_OtxToken') is not None else f"{Fore.RED}❌{Style.RESET_ALL} AlienVault Token"}
                : {f"{Fore.GREEN}✔{Style.RESET_ALL}  URLScan Token" if os.getenv('urlscan_token') is not None else f"{Fore.RED}❌{Style.RESET_ALL} URLScan Token"}
    """
    def __init__(self):
        super().__init__()
        self.console = Console(width=200)
    def default(self, query):
        response = self.CySecuAIfn.process_query_with_spinner(query)
        panel = Panel(Markdown(response, code_theme="monokai"), title="Secu-AI Response", title_align="left")
        self.console.print(panel)
    def do_addtriggers(self,arg):
        """Add trigger question for running tools"""
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'TriggeredList.json'), mode='r') as f:
            cybersecurity_enrichment_triggers = json.load(f)
            f.close()
        cybersecurity_enrichment_triggers.append(arg)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'TriggeredList.json'), mode='w') as f:
            json.dump(cybersecurity_enrichment_triggers,f)
            f.close()
        print("Added question in triggered list.")
    def do_clear(self, arg):
        """Clear the screen"""
        os.system('cls')
    def do_exit(self, arg):
        """Exit the Secu-AI."""
        print("Exiting the Secu-AI. Goodbye!")
        return True
    do_quit = do_exit
    do_EOF = do_exit
def main():
    CyberAssistantAI().cmdloop()
if __name__ == '__main__':
    main()