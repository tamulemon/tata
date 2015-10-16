
import os
import talib
import datetime
import numpy as np
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import commons
import talib.abstract as abstract
#def recognize(pattern_name, open, high, low, close, volume):
#    function = abstract.Function('cdl'+pattern_name)
#    window = commons.settings['pattern'][pattern_name]['window']
#    inputs = {
#        'open': open,
#        'high': high,
#        'low': low,
#        'close': close,
#        'volume': volume
#    }
#    ret = function(input)
#    for i in range(len(ret)-1,-1,-1):
#        if len(ret)-i > window:
#            return False,None
#        if ret[i] == 100:
#            print 'pattern found:',ticker,r.date[i],len(ret)-i
#            return True,len(ret)-i

def analyze_ticker(ticker):

    fh = open(commons.settings['data']['folder'] + '/' + ticker)
    # a numpy record array with fields: date, open, high, low, close, volume, adj_close)
    r = mlab.csv2rec(fh)
    fh.close()
    r.sort()
    
#    print recognize('morningstar', r.open, r.high, r.low, r.adj_close, r.volume)
    ret = talib.CDLMORNINGSTAR(r.open, r.high, r.low, r.adj_close)
    pattern_found = False
    for i in range(len(ret)-1,-1,-1):
        if len(ret)-i > commons.settings['pattern']['morningstar']['window']:
            break;
        if ret[i] == 100:
            print 'pattern found:',ticker,r.date[i],len(ret)-i
            pattern_found = True
            break;

    return pattern_found

tickers = os.listdir(commons.settings['data']['folder'])
count = 0
for ticker in tickers:
    if analyze_ticker(ticker):
        count = count + 1
