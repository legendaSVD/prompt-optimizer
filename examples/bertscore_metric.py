from prompt_optimizer.metric import BERTScoreMetric
from prompt_optimizer.poptim import StopWordOptim
prompt =
p_optimizer = StopWordOptim(metrics=[BERTScoreMetric()])
res = p_optimizer(prompt)
print(f"Optmized Prompt: {res.content}")
for key, value in res.metrics[0].items():
    print(f"{key}: {value:.3f}")