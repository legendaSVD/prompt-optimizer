import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from prompt_optimizer.poptim.base import PromptOptim
class LemmatizerOptim(PromptOptim):
    def __init__(self, verbose: bool = False, metrics: list = []):
        super().__init__(verbose, metrics)
        self.lemmatizer = WordNetLemmatizer()
        nltk.download("averaged_perceptron_tagger")
        nltk.download("wordnet")
    def get_wordnet_pos(self, word: str) -> str:
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {
            "J": wordnet.ADJ,
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV,
        }
        return tag_dict.get(tag, wordnet.NOUN)
    def optimize(self, prompt: str) -> str:
        words = prompt.split()
        lemmatized_words = [
            self.lemmatizer.lemmatize(word, self.get_wordnet_pos(word))
            for word in words
        ]
        opti_prompt = " ".join(lemmatized_words)
        return opti_prompt