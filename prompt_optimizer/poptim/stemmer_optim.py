from nltk.stem import PorterStemmer
from prompt_optimizer.poptim.base import PromptOptim
class StemmerOptim(PromptOptim):
    def __init__(self, verbose: bool = False, metrics: list = []):
        super().__init__(verbose, metrics)
        self.stemmer = PorterStemmer()
    def optimize(self, prompt: str) -> str:
        words = prompt.split()
        stemmed_words = [self.stemmer.stem(word) for word in words]
        opti_prompt = " ".join(stemmed_words)
        return opti_prompt