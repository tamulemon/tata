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

DATA_DIR = 'data/'
def analyze_ticker(ticker):

    fh = open(DATA_DIR + ticker)
    # a numpy record array with fields: date, open, high, low, close, volume, adj_close)
    r = mlab.csv2rec(fh)
    fh.close()
    r.sort()

    ### compute everything
    rsi = talib.RSI(r.adj_close)
    nslow = 26
    nfast = 12
    nema = 9
    macd, macdsignal, macdhist = talib.MACD(r.adj_close, fastperiod=nfast, slowperiod=nslow)
    ema = talib.EMA(macd, nema)

    if r[-1].volume < 5e5:
        return
    
    if rsi[-1] < 40 and macd[-1] < -0.5 and macd[-1] >= ema[-1] and macd[-2] < ema[-2]:
        print 'bullish crossover',ticker
        pattern_found = True
#    elif rsi[-1] > 50 and macd[-1] > 0.5 and macd[-1] <= ema[-1] and macd[-2] > ema[-2]:
#        print 'bearish crossover',ticker
#        pattern_found = True
    else:
        pattern_found = False

    if pattern_found:
        print 'macd',macd[-2],macd[-1]
        print 'ema',ema[-2],ema[-1]
        print 'rsi',rsi[-2],rsi[-1]
        angle = (macd[-1]-macd[-2]+ema[-2]-ema[-1])
        #print 'price',prices[-2],prices[-1]
        yahoo_url = 'http://finance.yahoo.com/echarts?s='+ticker+'+Interactive#{"showArea":false,"showLine":false,"showOhlc":true,"showEma":true,"emaColors":"#cc0000,#009999","emaPeriods":"10,50","emaWidths":"1,1","emaGhosting":"0,0","showMacd":true,"macdMacdWidth":"2","showRsi":true,"lineType":"bar","allowChartStacking":true}'
        stockcharts_url = 'http://stockcharts.com/h-sc/ui?s=' + ticker + '&p=D&yr=1&mn=0&dy=0&id=p53884104819'
        f.write('<tr>')
        f.write('<td>' + ticker + '</td>')
        f.write('<td>' + str(rsi[-1]) + '</td>')
        f.write('<td>' + str(angle) + '</td>')
        f.write('<td><a href="'+stockcharts_url+'">stockcharts</a>,<a href="'+yahoo_url+'">yahoo</a></td>')
        f.write('</tr>')
#        print 'http://finance.yahoo.com/echarts?s='+ticker+'+Interactive#{"showArea":false,"showLine":false,"showOhlc":true,"showEma":true,"emaColors":"#cc0000,#009999","emaPeriods":"10,50","emaWidths":"1,1","emaGhosting":"0,0","showMacd":true,"macdMacdWidth":"2","showRsi":true,"lineType":"bar","range":"6mo","allowChartStacking":true}'
        print ''
        #ticker_plotter.plot_ticker(ticker, r, rsi, macd, ema)

    ### more filters
    #volume > 1mil
    #rsi around or below 30
    #macd < -0.5
f = open('index.html', 'w')
f.write('<html><head><title>Stock Screener</title></head><body>')
f.write('<table>')
f.write('<tr><td>Name</td><td>rsi</td><td>angle</td><td>urls</td></tr>')
for ticker in os.listdir(DATA_DIR):
    analyze_ticker(ticker)
f.write('</table></body></html>')
f.close()
