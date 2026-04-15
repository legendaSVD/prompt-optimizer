from typing import Any, List
from prompt_optimizer.poptim.base import PromptOptim
from .utils import DotDict
class Sequential:
    def __init__(self, *optims: PromptOptim):
        self.optims: List[PromptOptim] = list(optims)
    def __call__(self, x: Any) -> Any:
        d = DotDict()
        d.content = x
        for optim in self.optims:
            d = optim(d.content)
        return d