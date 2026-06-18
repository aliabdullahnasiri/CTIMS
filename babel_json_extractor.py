import json

from babel.messages.extract import extract_python


def extract_json(fileobj, keywords, comment_tags, options):
    data = json.load(fileobj)

    def walk(obj):
        if isinstance(obj, dict):
            for value in obj.values():
                yield from walk(value)
        elif isinstance(obj, list):
            for item in obj:
                yield from walk(item)
        elif isinstance(obj, str):
            yield obj

    for text in walk(data):
        yield 0, None, text, []
