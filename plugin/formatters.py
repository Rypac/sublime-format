import json
from collections import OrderedDict


def format_json(input, settings=None):
    indent = 4
    if settings:
        indent = settings.get('tab_size', indent)
    try:
        data = json.loads(input, object_pairs_hook=OrderedDict)
        return json.dumps(data, indent=indent), None
    except ValueError:
        return None, 'Invalid JSON'
