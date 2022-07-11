# Time Tracker Extractor

Extracts hours worked across multiple workspaces in Clockify and Toggl. The time logs compiled are output as a CSV file grouped according to time period, user, and workspace.

## Getting Started

1. Install the script's dependencies. Python 3.7+ required.

```bash
pip install -r requirements.txt
```

2. Copy `tokens.example.json`, rename it to `tokens.json` and fill in the file with your API keys for either Toggl and/or Clockify. Multiple Toggl and Clockify tokens can be specified.

```json
{
    "toggl_tokens": [
        "TOGGL_TOKEN_GOES_HERE"
    ],
    "clockify_tokens": [
        "CLOCKIFY_TOKEN_GOES_HERE"
    ]
}
```

3. Run the `main.py` script to extract all times. For extra help, please consult the help dialogue with the `--help` flag.

```bash
python main.py
```

**Please Note** The time periods in this script run Wednesday to Friday and Friday to Wednesday. Modification of the script would be required to change this.

## License

MIT
