# -*- coding:utf-8 -*-

import json

from owlmixin import OwlMixin

from jumeaux.addons.dump import DumpExecutor
from jumeaux.models import DumpAddOnPayload


class Config(OwlMixin):
    default_encoding: str = 'utf8'
    force: bool = False


class Executor(DumpExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: DumpAddOnPayload) -> DumpAddOnPayload:
        content_type = payload.response.headers.get('content-type')
        mime_type = content_type.split(';')[0] if content_type else None
        encoding = payload.encoding.get_or(self.config.default_encoding)

        return DumpAddOnPayload.from_dict({
            "response": payload.response,
            "body": json.dumps(
                json.loads(payload.body.decode(encoding)),
                ensure_ascii=False, indent=4, sort_keys=True
            ).encode(encoding) if self.config.force or mime_type in ('text/json', 'application/json') else payload.body,
            "encoding": encoding
        })
