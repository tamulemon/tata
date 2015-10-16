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
import ticker_plotter
import json
import chaikin_money_flow
import commons
import shutil

def has_bullish_crossover(macd, macdhist, pastdays):
    return macd[-1-pastdays] < commons.settings['indicator']['bullish_crossover']['max_macd'] and macdhist[-1-pastdays] >= -0.2 and macdhist[-1-pastdays] <=0.2 and macdhist[-2-pastdays] < min(0, macdhist[-1-pastdays])

def has_pattern_detected(ret, window):
    pattern_found = False
    days_since_pattern_found = -1
    for i in range(len(ret)-1,len(ret)-window,-1):
        if ret[i] == 100:
            pattern_found = True
            days_since_pattern_found = len(ret)-1-i
            break;
    return pattern_found, days_since_pattern_found
def analyze_ticker(ticker, scan_type, index):

    fh = open(commons.settings['data']['folder'] + '/' + ticker)
    # a numpy record array with fields: date, open, high, low, close, volume, adj_close)
    r = mlab.csv2rec(fh)
    fh.close()
    r.sort()

    ### compute everything
    rsi = talib.RSI(r.adj_close, commons.settings['rsi']['timeperiod'])
    cmf = chaikin_money_flow.CMF(r, commons.settings['cmf']['timeperiod'])
    macd, macdsignal, macdhist = talib.MACD(r.adj_close, fastperiod=commons.settings['macd']['fastperiod'], slowperiod=commons.settings['macd']['slowperiod'], signalperiod=commons.settings['macd']['signalperiod'])

    ### basic filter
    if r[-1].adj_close < 10:
        return False
    
    if r[-1].volume < 5e5:
        return False

    if scan_type == 0:
        if rsi[-1] > commons.settings['indicator']['relative_strength']['max_rsi']:
            return False

        pattern_found = True
        days_since_pattern_found = 0

    elif scan_type == 1:
        if cmf[-1] < commons.settings['indicator']['money_flow']['min_cmf']:
            return False

        if macdhist[-1] < 0:
            return False

        pattern_found = False
        days_since_pattern_found = -1
        for days in range(0,commons.settings['indicator']['bullish_crossover']['window']):
            if has_bullish_crossover(macd, macdhist, days):
                pattern_found = True
                days_since_pattern_found = days
                break

    elif scan_type == 2:
        ret = talib.CDLMORNINGSTAR(r.open, r.high, r.low, r.adj_close)
        pattern_found, days_since_pattern_found = has_pattern_detected(ret, commons.settings['pattern']['default']['window'])
    elif scan_type == 3:
        ret = talib.CDLENGULFING(r.open, r.high, r.low, r.adj_close)
        pattern_found, days_since_pattern_found = has_pattern_detected(ret, commons.settings['pattern']['default']['window'])
    elif scan_type == 4:
        ret = talib.CDLDRAGONFLYDOJI(r.open, r.high, r.low, r.adj_close)
        pattern_found, days_since_pattern_found = has_pattern_detected(ret, commons.settings['pattern']['default']['window'])
    elif scan_type == 5:
        ret = talib.CDLPIERCING(r.open, r.high, r.low, r.adj_close)
        pattern_found, days_since_pattern_found = has_pattern_detected(ret, commons.settings['pattern']['default']['window'])

    if pattern_found:
        angle = (macd[-1-days_since_pattern_found]-macd[-2-days_since_pattern_found]+macdsignal[-2-days_since_pattern_found]-macdsignal[-1-days_since_pattern_found])
        #print 'price',prices[-2],prices[-1]
        yahoo_url = 'http://finance.yahoo.com/echarts?s=%s+Interactive#{"showArea":false,"useLogScale":true,"showLine":false,"showOhlc":true,"showMacd":true,"macdSignalSmoothing":7,"showRsi":true,"rsiPeriod":2,"lineType":"bar","range":"6mo","didDisablePrePost":true,"allowChartStacking":true}'%(ticker)
        stockcharts_url = 'http://stockcharts.com/h-sc/ui?s=' + ticker + '&p=D&yr=0&mn=6&dy=0&id=p30441120775'
        if index % 2 == 0:
            f.write('<tr class="even">')
        else:
            f.write('<tr>')
        f.write('<td>' + ticker + '</td>')        
        f.write('<td>' + str(r.adj_close[-1]) + '</td>')
        f.write('<td>' + str(cmf[-1]) + '</td>')
        f.write('<td>' + str(rsi[-1]) + '</td>')
        f.write('<td>' + str(angle) + '</td>')
        f.write('<td>' + str(days_since_pattern_found) + '</td>')
        f.write('<td><a href="'+stockcharts_url+'">stockcharts</a>,<a href="'+yahoo_url+'">yahoo</a></td>')
        f.write('</tr>')
        #ticker_plotter.plot_ticker(ticker, r, rsi, cmf, macd, macdsignal)

    return pattern_found

def scan(scan_type):
    f.write('<h3>'+commons.scan_type_descriptions[scan_type]+'</h3>')
    f.write('<table>')
    f.write('<tr><th>Name</th><th>Price</th><th>CMF</th><th>RSI</th><th>Angle</th><th>#Days</th><th>URLs</th></tr><tbody>')
    tickers = os.listdir(commons.settings['data']['folder'])
    count = 0
    for ticker in tickers:
        if analyze_ticker(ticker, scan_type, count):
            count = count + 1
    f.write('</tbody></table>')

f = open('index.html', 'w')
f.write('<html><head><title>Stock Screener</title><link href="/style.css" rel="stylesheet" type="text/css"></head><body>')

for t in range(0, len(commons.scan_type_descriptions)):
    scan(t)

f.write('</body></html>')
shutil.copy2(f.name, 'history/index'+ datetime.date.today().strftime('-%Y-%m-%d') + '.html')
f.close()

