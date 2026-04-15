import copy
from abc import ABC, abstractmethod
from .logger import logger
from .utils import DotDict, protected_runner
class PromptOptim(ABC):
    def __init__(
        self, verbose: bool = False, metrics: list = [], protect_tag: str = None
    ):
        self.verbose = verbose
        self.metrics = metrics
        self.protect_tag = protect_tag
    @abstractmethod
    def optimize(self, prompt: str) -> str:
        pass
    @protected_runner
    def run(self, prompt: str) -> str:
        return self.optimize(prompt)
    def run_json(self, json_data: list, skip_system: bool = False) -> dict:
        optim_json_data = copy.deepcopy(json_data)
        for data in optim_json_data:
            if skip_system and data["role"] == "system":
                continue
            data["content"] = self.run(data["content"])
        return optim_json_data
    def run_langchain(self, langchain_data: list, skip_system: bool = False):
        optim_langchain_data = copy.deepcopy(langchain_data)
        for data in optim_langchain_data:
            if skip_system and data.type == "system":
                continue
            data.content = self.run(data.content)
        return optim_langchain_data
    def __call__(
        self,
        prompt_data: list,
        skip_system: bool = False,
        json: bool = False,
        langchain: bool = False,
    ) -> list:
        assert not (json and langchain), "Data type can't be both json and langchain"
        if skip_system:
            assert (
                json or langchain
            ), "Can't skip system prompts without batched json format"
        if json:
            opti_prompt_data = self.run_json(prompt_data, skip_system)
        elif langchain:
            opti_prompt_data = self.run_langchain(prompt_data, skip_system)
        else:
            opti_prompt_data = self.run(prompt_data)
        metric_results = []
        for metric in self.metrics:
            if json or langchain:
                metric_result = metric.batch_run(
                    prompt_data, opti_prompt_data, skip_system, json, langchain
                )
            else:
                metric_result = metric.run(prompt_data, opti_prompt_data)
            metric_results.append(metric_result)
        if self.verbose:
            logger.info(f"Prompt Data Before: {prompt_data}")
            logger.info(f"Prompt Data After: {opti_prompt_data}")
            for metric_result in metric_results:
                for key in metric_result:
                    logger.info(f"{key}: {metric_result[key]:.3f}")
        result = DotDict()
        result.content = opti_prompt_data
        result.metrics = metric_results
        return result