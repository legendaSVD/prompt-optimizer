import nltk
from prompt_optimizer.poptim.base import PromptOptim
class NameReplaceOptim(PromptOptim):
    def __init__(self, verbose: bool = False, metrics: list = []):
        super().__init__(verbose, metrics)
        self.opti_names = self.get_opti_names()
    def download(self):
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")
        nltk.download("maxent_ne_chunker")
        nltk.download("words")
    def process(self, text: str) -> nltk.Tree:
        tokens = nltk.tokenize.word_tokenize(text)
        pos = nltk.pos_tag(tokens)
        sentence_tree = nltk.ne_chunk(pos, binary=False)
        return sentence_tree
    def get_opti_names(self) -> list:
        opti_names =
        opti_names = [name.strip() for name in opti_names.split()]
        return opti_names
    def gen_name_map(self, text: str) -> dict:
        name_list = []
        try:
            sentence_tree = self.process(text)
        except Exception:
            self.download()
            sentence_tree = self.process(text)
        for subtree in sentence_tree.subtrees(filter=lambda t: t.label() == "PERSON"):
            person = []
            name = ""
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 1:
                for part in person:
                    name += part + " "
                name = name.strip()
                if name not in name_list:
                    name_list.append(name)
        mapping = dict(zip(name_list[: len(self.opti_names)], self.opti_names))
        return mapping
    def opti_name_replace(self, text: str, mapping: dict) -> str:
        for old_name in mapping:
            new_name = mapping[old_name]
            text = text.replace(old_name, new_name)
        return text
    def optimize(self, prompt: str) -> str:
        mapping = self.gen_name_map(prompt)
        opti_prompt = self.opti_name_replace(prompt, mapping)
        return opti_prompt