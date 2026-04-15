from autocorrect import Speller
from prompt_optimizer.poptim.base import PromptOptim
class AutocorrectOptim(PromptOptim):
    def __init__(self, fast: bool = False, verbose: bool = False, metrics: list = []):
        super().__init__(verbose, metrics)
        self.spell = Speller(lang="en", fast=fast)
    def optimize(self, prompt: str) -> str:
        words = prompt.split()
        autocorrected_words = [self.spell(word) for word in words]
        opti_prompt = " ".join(autocorrected_words)
        return opti_prompt