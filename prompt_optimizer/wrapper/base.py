from abc import ABC, abstractmethod
class Wrapper(ABC):
    def __init__(self, db_manager, poptimizer):
        self.db_manager = db_manager
        self.poptimizer = poptimizer
    @abstractmethod
    def wrap(self, *args, **kwargs):
        pass