from prompt_optimizer.poptim import PunctuationOptim
prompt =
p_optimizer = PunctuationOptim(verbose=True, protect_tag="pt")
optimized_prompt = p_optimizer(prompt).content
print("optimized_prompt: ", optimized_prompt)