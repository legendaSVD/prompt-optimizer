import string
from prompt_optimizer.poptim.base import PromptOptim
class PunctuationOptim(PromptOptim):
    def __init__(self, verbose: bool = False, metrics: list = [], **kwargs):
        super().__init__(verbose, metrics, **kwargs)
    def optimize(self, prompt: str) -> str:
        opti_prompt = prompt.translate(str.maketrans("", "", string.punctuation))
        return opti_prompt