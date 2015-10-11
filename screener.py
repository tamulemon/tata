import urllib2
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ochl
import matplotlib
import pylab
matplotlib.rcParams.update({'font.size': 9})

evenBetter = ['AWH', 'AFAM', 'ACAS', 'ASI', 'NLY', 'ANH', 'AIZ', 'AXS', 'BHLB', 'COF', 'CMO', 'DYN', 'FDEF', 'HMN', 'IM', 'IRDM', 'KMPR', 'LNC', 'LMIA', 'MANT', 'MCGC', 'MRH', 'MVC', 'NAVG', 'OVTI', 'PRE', 'PMC', 'PJC', 'PTP', 'BPOP', 'PL', 'RF', 'SKYW', 'STI', 'SPN', 'SYA', 'TECD', 'TSYS', 'TITN', 'TPC', 'UNM', 'VOXX', 'XL']

def moving_average(x, n, type='simple'):
    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    x = np.asarray(x)
    if type=='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()


    a =  np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a

def relative_strength(prices, n=14):
    """
    compute the n period relative strength indicator
    http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
    http://www.investopedia.com/terms/r/rsi.asp
    """

    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi

def moving_average_convergence(x, nslow=26, nfast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    """
    emaslow = moving_average(x, nslow, type='exponential')
    emafast = moving_average(x, nfast, type='exponential')
    return emaslow, emafast, emafast - emaslow

def computeRSI(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi

def computeSMA(values,window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array

########EMA CALC ADDED############
def computeEMA(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def computeMACD(x, slow=26, fast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    """
    emaslow = computeEMA(x, slow)
    emafast = computeEMA(x, fast)
    return emaslow, emafast, emafast - emaslow

def plotGraph(stock, date, SP, prices, volume, sma1, sma2, smap1, smap2, rsi, macd, ema9):
    try:   
        fig = plt.figure(facecolor='#07000d')

        ax1 = plt.subplot2grid((9,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
        candlestick_ochl(ax1, prices[-SP:], width=.6, colorup='#53c156', colordown='#ff1717')

        Label1 = str(smap1)+' SMA'
        Label2 = str(smap2)+' SMA'

        ax1.plot(date[-SP:],sma1[-SP:],'#e1edf9',label=Label1, linewidth=1.5)
        ax1.plot(date[-SP:],sma2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
        
        ax1.grid(True, color='w')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.yaxis.label.set_color("w")
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.tick_params(axis='y', colors='w')
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors='w')
        plt.ylabel('Stock price and Volume')

        maLeg = plt.legend(loc=9, ncol=2, prop={'size':7},
                   fancybox=True, borderaxespad=0.)
        maLeg.get_frame().set_alpha(0.4)
        textEd = pylab.gca().get_legend().get_texts()
        pylab.setp(textEd[0:5], color = 'w')

        volumeMin = 0
        
        ax0 = plt.subplot2grid((9,4), (0,0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')

        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'
        
        ax0.plot(date[-SP:], rsi[-SP:], rsiCol, linewidth=1.5)
        ax0.axhline(70, color=negCol)
        ax0.axhline(30, color=posCol)
        ax0.fill_between(date[-SP:], rsi[-SP:], 70, where=(rsi[-SP:]>=70), facecolor=negCol, edgecolor=negCol, alpha=0.5)
        ax0.fill_between(date[-SP:], rsi[-SP:], 30, where=(rsi[-SP:]<=30), facecolor=posCol, edgecolor=posCol, alpha=0.5)
        ax0.set_yticks([30,70])
        ax0.yaxis.label.set_color("w")
        ax0.spines['bottom'].set_color("#5998ff")
        ax0.spines['top'].set_color("#5998ff")
        ax0.spines['left'].set_color("#5998ff")
        ax0.spines['right'].set_color("#5998ff")
        ax0.tick_params(axis='y', colors='w')
        ax0.tick_params(axis='x', colors='w')
        plt.ylabel('RSI')

        ax1v = ax1.twinx()
        ax1v.fill_between(date[-SP:],volumeMin, volume[-SP:], facecolor='#00ffe8', alpha=.4)
        ax1v.axes.yaxis.set_ticklabels([])
        ax1v.grid(False)
        ###Edit this to 3, so it's a bit larger
        ax1v.set_ylim(0, 3*volume.max())
        ax1v.spines['bottom'].set_color("#5998ff")
        ax1v.spines['top'].set_color("#5998ff")
        ax1v.spines['left'].set_color("#5998ff")
        ax1v.spines['right'].set_color("#5998ff")
        ax1v.tick_params(axis='x', colors='w')
        ax1v.tick_params(axis='y', colors='w')

        ax2 = plt.subplot2grid((9,4), (5,0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')
        fillcolor = '#00ffe8'
        ax2.plot(date[-SP:], macd[-SP:], color='#4ee6fd', lw=2)
        ax2.plot(date[-SP:], ema9[-SP:], color='#e1edf9', lw=1)
        ax2.fill_between(date[-SP:], macd[-SP:]-ema9[-SP:], 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)

        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax2.spines['bottom'].set_color("#5998ff")
        ax2.spines['top'].set_color("#5998ff")
        ax2.spines['left'].set_color("#5998ff")
        ax2.spines['right'].set_color("#5998ff")
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w')
        plt.ylabel('MACD', color='w')
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))

        plt.suptitle(stock,color='w')

        plt.setp(ax0.get_xticklabels(), visible=False)
        ### add this ####
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        
        #plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
        plt.show()
        fig.savefig('example.png',facecolor=fig.get_facecolor())    
    except Exception,e:
        print 'plotGraph',str(e)

###############################
def graphData(stock,nsma1,nsma2):
    #######################################
    # Pulling data
    #######################################
    try:
        print 'Currently Pulling', stock
        
        print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
        #Keep in mind this is close high low open, lol. 
        urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=1y/csv'
        stockFile =[]
        try:
            sourceCode = urllib2.urlopen(urlToVisit).read()
            splitSource = sourceCode.split('\n')
            for eachLine in splitSource:
                splitLine = eachLine.split(',')
                if len(splitLine)==6:
                    if 'values' not in eachLine:
                        stockFile.append(eachLine)
        except Exception, e:
            print str(e), 'failed to organize pulled data.'
    except Exception,e:
        print str(e), 'failed to pull pricing data'

    #######################################
    # Plotting data
    #######################################
    try:   
        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True, converters={ 0: mdates.strpdate2num('%Y%m%d')})
        x = 0
        y = len(date)
        prices = []
        while x < y:
            appendLine = date[x],openp[x],closep[x],highp[x],lowp[x],volume[x]
            prices.append(appendLine)
            x+=1
            
        sma1 = moving_average(closep, nsma1)
        sma2 = moving_average(closep, nsma2)
        SP = len(date[nsma2-1:])
        rsi = relative_strength(closep)
        nslow = 26
        nfast = 12
        nema = 9
        emaslow, emafast, macd = moving_average_convergence(closep)
        ema9 = moving_average(macd, nema, type='exponential')
        if macd[-1] >= ema9[-1] and macd[-2] < ema9[-2]:
            print 'bullish crossover'
        elif macd[-1] <= ema9[-1] and macd[-2] > ema9[-2]:
            print 'bearish crossover'
        else:
            print 'no clear pattern'
            print 'macd',macd[-2],macd[-1]
            print 'ema9',ema9[-2],ema9[-1]
            print 'rsi',rsi[-2],rsi[-1]
            print 'price',prices[-2],prices[-1]
            print 'date', date[-2],date[-1]
        plotGraph(stock, date, SP, prices, volume, sma1, sma2, nsma1, nsma2, rsi, macd, ema9)
           
    except Exception,e:
        print 'main loop',str(e)









def screener(stock, prescreen):
    try:
        print 'doing',stock
        sourceCode = urllib2.urlopen('http://finance.yahoo.com/q/ks?s='+stock).read()
        pbr = sourceCode.split('Price/Book (mrq):</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
        print 'price to book ratio:',stock,pbr
        if prescreen and float(pbr) >= 1:
            print 'price to book ratio too high:',stock,pbr
            return
        
        PEG5 = sourceCode.split('PEG Ratio (5 yr expected)<font size="-1"><sup>1</sup></font>:</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
        if prescreen and (0 >= float(PEG5) or float(PEG5) >= 2):
            print 'PEG forward 5 years too high:',stock,PEG5
            return

        DE = sourceCode.split('Total Debt/Equity (mrq):</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
        if prescreen and (0 >= float(DE) or float(DE) >= 2):
            print 'Debt to Equity too high:',stock,DE
            return

        PE12 = sourceCode.split('Trailing P/E (ttm, intraday):</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
        if prescreen and float(PE12) >= 15:
            print 'Trailing PE (12mo) too high:',stock,PE12

        print '______________________________________'
        print ''
        print stock,'meets requirements'
        print 'price to book:',pbr
        print 'PEG forward 5 years',PEG5
        print 'Trailing PE (12mo):',PE12
        print 'Debt to Equity:',DE
        print '______________________________________'

        try:
            graphData(stock,25,50)

        except Exception, e:
            print 'failed the main quandl loop for reason of',str(e)


            
    except Exception,e:
        print 'failed in the main loop',str(e)
        #pass

screener('JNJ', False)