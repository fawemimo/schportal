from django.http import QueryDict
from rest_framework import parsers
import json

class MultipartJsonParser(parsers.MultiPartParser):
    # https://stackoverflow.com/a/50514022/8897256
    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = {}
        data = json.loads(result.data)
        qdict = QueryDict('', mutable=True)
        qdict.update(data)
        return parsers.DataAndFiles(qdict, result.files)