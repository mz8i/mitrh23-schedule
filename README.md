## Requirements
- `jq`
- Python 3 (no third-party libraries required)

## Usage

1. Get raw data from Notion
    1. Go to [MIT RH 23 Notion Schedule](https://mitrealityhack.notion.site/aaa49b488efe433bb1e8386b673722c3?v=7594562b1170427bb301a5b0b835b7a7)
    2. Open Dev Tools (F12) > Network Tab
    3. Find a request to a URL like `https://mitrealityhack.notion.site/api/v3/queryCollection?src=initial_load`, the transferred size of the response is ~22kB - save the raw response content locally (inside this repository) as `data/schedule.json`
2. Run the following jq script in terminal to get preprocessed schedule data:
```bash
jq '.recordMap.block | to_entries | map({id:.key, properties: (.value.value.properties)})' data/schedule.json > data/preprocessed.json
```
3. Run the following jq script in terminal to get preprocessed Notion data schema:
```bash
jq '.recordMap.collection | to_entries | .[0].value.value.schema | map_values({name:.name, type: .type, options: (if (.options == null) then null else .options | map(.value) end)})' data/schedule.json > data/schema.json
```

4. Run the python `process` script to get the processed JSON output:
```bash
python3 ./process.py
```

5. To get the data in a CSV format suitable for importing to Google Calendar, run the `make_csv` python script:
```bash
python3 ./make_csv.py
```

6. Import CSV into Google Calendar through a desktop browser as described [here](https://support.google.com/calendar/answer/37118?hl=en&co=GENIE.Platform%3DDesktop). That site also documents the CSV file format for importing calendar events.

## NOTES / CAUTIONS
- the CSV output doesn't contain time zone info. Your calendar needs to be set to the same local timezone as the event schedule when importing the CSV, so that the dates are imported correctly
- the `Location` column gets imported into Google Calendar using Google Maps. Currently, the location codes are mapped to map locations in Polish (especially the USA country name is in Polish in `process.py` and in `example-data/` files). Not sure if this won't work for someone using the calendar in a different language - might need adjusting
