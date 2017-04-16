import json
from collections import OrderedDict


def format_json(input):
    try:
        data = json.loads(input, object_pairs_hook=OrderedDict)
        return json.dumps(data, indent=4), None
    except ValueError:
        return None, 'Invalid JSON'
