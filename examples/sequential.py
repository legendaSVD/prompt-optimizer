from prompt_optimizer.metric import TokenMetric
from prompt_optimizer.poptim import (
    AutocorrectOptim,
    LemmatizerOptim,
    PunctuationOptim,
    Sequential,
)
prompt =
p_optimizer = Sequential(
    LemmatizerOptim(metrics=[TokenMetric()]),
    PunctuationOptim(metrics=[TokenMetric()]),
    AutocorrectOptim(metrics=[TokenMetric()]),
)
optimized_prompt = p_optimizer(prompt)
print(optimized_prompt)