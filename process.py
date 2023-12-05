#!/usr/bin/env python3
import json
from pathlib import Path

preproc = json.loads(Path('data/preprocessed.json').read_text())
schema = json.loads(Path('data/schema.json').read_text())

def unpack_value(val, is_datetime):
    return val[0][1][0][1] if is_datetime else val[0][0]

def process_property(key, value, schema):
    prop_schema = schema.get(key, None)

    if prop_schema is None:
        return key, None

    return prop_schema['name'].strip(), unpack_value(value, prop_schema['type'] == 'date')

def process_event(evt, schema):
    print('1')
    property_keyvalues = [process_property(key, value, schema) for (key,value) in evt['properties'].items() ]
    return {
            'id': evt['id'],
            'properties': {
                k: v for (k,v) in property_keyvalues if v is not None
            }
            }

processed = [process_event(evt, schema) for evt in preproc if evt['properties'] != None]

Path('data/output.json').write_text(json.dumps(processed, indent=4))