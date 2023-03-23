# Daisy - A transport telegram bot

Daisy can provide UK train times, and TfL service status for London transport. It is built around the TfL and Realtime Trains APIs.

## Installation
Daisy relies on the python-telegram-bot module. Can be installed with the following command:

`python3 -m pip install python-telegram-bot`

Daisy also relies on having API keys for Telegram, and Realtime Trains. Create a daisySecrets.py with the following variable names:

```python
rttuser
rttpass
bot_token
```

You can now finally start the bot with `python3 main.py`
