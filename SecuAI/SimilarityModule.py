from sentence_transformers import SentenceTransformer, util
import torch, os, json

class IsAPIRequest:
    def __init__(self) -> None:
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        with open(os.path.join(self.script_dir,'TriggeredList.json'), mode='r') as f:
            self.cybersecurity_enrichment_triggers = json.load(f)
            f.close()
        self.trigger_embeddings = self.model.encode(self.cybersecurity_enrichment_triggers)
        self.threshold = 0.65
    def check(self,user_query):
        user_query_embedding = self.model.encode(user_query)
        cosine_scores = util.cos_sim(user_query_embedding, self.trigger_embeddings)
        max_similarity = torch.max(cosine_scores).item()
        if max_similarity >= self.threshold:
            return True
        else:
            return False