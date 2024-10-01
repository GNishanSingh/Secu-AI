from SecuAI.Enricher.VirusTotal import VirusTotal
from SecuAI.Enricher.WindowsData import WindowsLogs
from SecuAI.Enricher.AlienVault import AlienVaultOTX
from SecuAI.Enricher.URLScan import URLScan
from SecuAI.Enricher.WhoisLookup import WhoIsLookUp
import os, json
from dotenv import load_dotenv
import functools

load_dotenv()
class MistralToolAI:
    def __init__(self,client) -> None:
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.AlienVault = AlienVaultOTX(os.getenv('AlienVault_OtxToken'))
        self.URLScan = URLScan(os.getenv('urlscan_token'))
        self.vtlookup = VirusTotal(os.getenv("VirusTotal_Token"))
        self.QueryLogs = WindowsLogs()
        self.whoisquery = WhoIsLookUp()
        self.nametofunction = {
                'CheckVirusTotal': functools.partial(self.vtlookup.query),
                'QueryLogs': functools.partial(self.QueryLogs.query_event_log),
                'AlienVault':functools.partial(self.AlienVault.query),
                'URLScan':functools.partial(self.URLScan.query),
                'WhoIs': functools.partial(self.whoisquery.query)
        }
        with open(os.path.join(self.script_dir,'FuncTools.json'), mode='r') as f:
            self.cybtools = json.load(f)
            f.close()
        self.MistralAgent = os.getenv("MistralAgent")
        self.client = client
    def getfunctiondetails (self, data):
            chat_response = self.client.agents.complete(
                agent_id = self.MistralAgent,
                messages = [
                    {
                        "role": "user",
                        "content": json.dumps(data),
                    },
                ],
                tools=self.cybtools,
                tool_choice='any'
            )
            fundata = []
            for resp in chat_response.choices[0].message.tool_calls:
                fundata.append(
                     {
                          "role":"user",
                          "name":resp.function.name,
                          "content":f"User Query:{data}\n\nFunctionData:"+'\n\n'+json.dumps(self.nametofunction[resp.function.name](json.loads(resp.function.arguments))),
                          "tool_call_id":resp.id
                     }
                )
            return self.client.agents.complete(
                     agent_id=self.MistralAgent,
                     messages=fundata
                ).choices[0].message.content