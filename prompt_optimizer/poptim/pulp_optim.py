from pulp import LpBinary, LpMinimize, LpProblem, LpVariable, lpSum
from prompt_optimizer.poptim.base import PromptOptim
class PulpOptim(PromptOptim):
    def __init__(self, p: float = 0.1, verbose: bool = False, metrics: list = []):
        super().__init__(verbose, metrics)
        self.aggression = p
    def optimize(self, prompt: str) -> str:
        tokens = prompt.split()
        target_length = int(len(tokens) * (1 - self.aggression))
        x = LpVariable.dicts("x", range(len(tokens)), cat=LpBinary)
        model = LpProblem("Extractive Compression", LpMinimize)
        model += lpSum([1 - x[i] for i in range(len(tokens))])
        model += lpSum([x[i] for i in range(len(tokens))]) == target_length
        for i in range(len(tokens)):
            for j in range(i + 1, len(tokens)):
                if tokens[i] == tokens[j]:
                    model += x[i] <= x[j]
        model.solve()
        selected_indices = [i for i in range(len(tokens)) if x[i].value() == 1]
        opti_prompt = " ".join([tokens[i] for i in selected_indices])
        return opti_prompt