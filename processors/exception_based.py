from typing import Optional, Type

from sentry_tagger.enums import Target
from sentry_tagger.processors.base import BaseProcessor


class ExceptionBasedProcessor(BaseProcessor):

    REGISTRY = {}

    @classmethod
    def register(cls, exc_class: Type[Exception], target: Target):
        cls.REGISTRY[exc_class] = target

    def tag(self, event: dict, hint: dict) -> Optional[Target]:
        exc_class = self.exception_class_from_hint(hint)
        if exc_class in self.REGISTRY:
            return self.REGISTRY[exc_class]
        return None


def register(target: Target):

    def inner(exc_class: Type[Exception]):
        ExceptionBasedProcessor.register(exc_class, target)
        return exc_class

    return inner
