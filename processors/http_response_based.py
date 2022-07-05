from typing import Optional

from requests import HTTPError

from sentry_tagger.enums import Target
from sentry_tagger.processors.base import BaseProcessor


class HttpResponseBasedProcessor(BaseProcessor):
    STATUS_CODE_MAP = {
        401: Target.USER,
        500: Target.SYSTEM,
    }

    def tag(self, event: dict, hint: dict) -> Optional[Target]:
        exception = self.exception_from_hint(hint)
        if isinstance(exception, HTTPError):
            code = exception.response.status_code
            if code in self.STATUS_CODE_MAP:
                return self.STATUS_CODE_MAP[code]

