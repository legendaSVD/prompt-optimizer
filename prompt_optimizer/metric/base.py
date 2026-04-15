from abc import ABC, abstractmethod
from collections import defaultdict
class Metric(ABC):
    def __init__(self):
        self.key = None
    @abstractmethod
    def run(self, prompt_before: str, prompt_after: str) -> dict:
        pass
    def run_json(self, json_data_before: dict, json_data_after: dict) -> dict:
        res = self.run(json_data_before["content"], json_data_after["content"])
        return res
    def batch_run(
        self,
        prompts_before: list,
        prompts_after: list,
        skip_system: bool = False,
        json: bool = False,
        langchain: bool = False,
    ) -> float:
        avg_m = defaultdict(float)
        n = 0
        for pb, pa in zip(prompts_before, prompts_after):
            if json:
                if skip_system and pb["role"] == "system":
                    continue
                else:
                    res = self.run_json(pb, pa)
                    n += 1
            elif langchain:
                if skip_system and pb.role == "system":
                    continue
                else:
                    res = self.run(pb.content, pa.content)
                    n += 1
            else:
                res = self.run(pb, pa)
                n += 1
            for key in res:
                avg_m[key] += res[key]
        for key in avg_m:
            avg_m[key] /= n
        return avg_m
    def __call__(self, prompt_before: str, prompt_after: str) -> dict:
        return self.run(prompt_before, prompt_after)