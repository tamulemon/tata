import json

global  settings

try:
  settings
except NameError:
  settings = json.load(open('settings.json'))

global scan_type_descriptions
scan_type_descriptions = ['RSI-Based', 'MACD-Based', 'Morning Star Pattern', 'Engulfing Pattern', 'Dragonfly Doji Pattern', 'PIERCING Pattern']