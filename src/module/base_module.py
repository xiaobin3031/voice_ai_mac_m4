"""基础模块"""

from abc import ABC, abstractmethod

class BaseModule(ABC):

    def __init__(self): pass

    @abstractmethod
    def first(self, text): pass

    @abstractmethod
    def again(self, text): pass