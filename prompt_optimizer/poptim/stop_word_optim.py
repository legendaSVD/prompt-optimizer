import nltk
from prompt_optimizer.poptim.base import PromptOptim
class StopWordOptim(PromptOptim):
    def __init__(self, verbose: bool = False, metrics: list = []):
        super().__init__(verbose, metrics)
        try:
            self.stop_words = set(nltk.corpus.stopwords.words("english"))
        except Exception:
            nltk.download("stopwords")
            self.stop_words = set(nltk.corpus.stopwords.words("english"))
    def optimize(self, prompt: str) -> str:
        words = prompt.split()
        filtered_words = [word for word in words if word.lower() not in self.stop_words]
        opti_prompt = " ".join(filtered_words)
        return opti_prompt