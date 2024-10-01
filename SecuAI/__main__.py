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
from rich.progress import SpinnerColumn, Progress
from dotenv import load_dotenv
from SecuAI.SimilarityModule import IsAPIRequest
from SecuAI.toolsAI import MistralToolAI

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
                    "content": json.dumps(data),
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
        with Progress(SpinnerColumn(),transient=True) as progress:
            task = progress.add_task("[cyan]Analyzing...",total=None)
            try:
                response = self.process_query(query)
            finally:
                sys.stdout.flush()
            progress.stop_task(task)
        return response

class CyberAssistantAI(cmd.Cmd):
    CySecuAIfn = CybSecuAI()
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
{Fore.BLUE}Version{Style.RESET_ALL}     : v1.3
{Fore.BLUE}Description{Style.RESET_ALL} : Cybersecurity AI assistant for making SOC analyst life easier.
{Fore.BLUE}Author{Style.RESET_ALL}      : Gurmukhnishan Singh
{Fore.BLUE}Email{Style.RESET_ALL}       : gurmukhnishansingh@gmail.com
    """
    def __init__(self):
        super().__init__()
        self.console = Console(width=300)
    def default(self, query):
        response = self.CySecuAIfn.process_query_with_spinner(query)
        self.console.print(Markdown(response, code_theme="manni"))
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