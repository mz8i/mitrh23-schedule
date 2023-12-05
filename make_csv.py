import json
import csv
from pathlib import Path


events = json.loads(Path('data/output.json').read_text())

csvrows = []

def get_location(loc: str):
    if "iHQ" in loc:
        return "MIT Innovation Headquarters, 292 Main St, Cambridge, MA 02142, Stany Zjednoczone"
    elif "ML" in loc:
        return "MIT Media Lab, 75 Amherst St, Cambridge, MA 02139, Stany Zjednoczone"


for e in events:
    print(e['id'])
    evt = e['properties']
    dt = evt['Date and Time']
    loc = evt['Location']
    loc_short = loc.split('|')[0].strip()
    major = evt.get('Major', None)
    row = {
        'Subject': f"{evt['Workshop Name']} [{major} / {loc_short}]",
        'Start Date': dt['start_date'],
        'Start Time': dt['start_time'],
        'End Date': dt['end_date'],
        'End Time': dt['end_time'],
        'All Day Event': 'False',
        'Location': get_location(loc),
        'Description': f"""
Location: {loc}
{f"Major: {major}" if major is not None else "" }

{evt.get('Topics / Description', '')}
Speaker: {evt['Speaker']}
{f"Type: {evt['Type']}" if 'Type' in evt else ""}
{f"Status: {evt['Status']}" if 'Status' in evt else ""}
"""
    }
    csvrows.append(row)

keys = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'All Day Event', 'Location', 'Description']

with Path('data/events.csv').open('w') as f:
    dict_writer =csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(csvrows)