from typing import Optional, Type

from sentry_tagger.enums import Target


class BaseProcessor:
    def tag(self, event: dict, hint: dict) -> Optional[Target]:
        raise NotImplementedError

    @staticmethod
    def exception_class_from_hint(hint: dict) -> Optional[Type[Exception]]:
        return hint.get('exc_info', [None])[0]

    @staticmethod
    def exception_from_hint(hint: dict) -> Optional[Exception]:
        return hint.get('exc_info', [None, None])[1]
