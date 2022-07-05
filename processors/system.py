from typing import Optional

from sentry_tagger.enums import Target
from sentry_tagger.processors.base import BaseProcessor


class SystemTagProcessor(BaseProcessor):
    def tag(self, event: dict, hint: dict) -> Optional[Target]:
        return Target.SYSTEM

