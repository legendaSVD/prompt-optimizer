import tiktoken
from prompt_optimizer.metric.base import Metric
class TokenMetric(Metric):
    def __init__(self, tokenizer: str = "cl100k_base"):
        super().__init__()
        self.tokenizer = tiktoken.get_encoding(tokenizer)
        self.key = "num_token_opti_ratio"
    def run(self, prompt_before: str, prompt_after: str) -> dict:
        n_tokens_before = len(self.tokenizer.encode(prompt_before))
        n_tokens_after = len(self.tokenizer.encode(prompt_after))
        opti_ratio = (n_tokens_before - n_tokens_after) / n_tokens_before
        return {self.key: opti_ratio}
    def __call__(self, prompt_before: str, prompt_after: str) -> dict:
        return self.run(prompt_before, prompt_after)