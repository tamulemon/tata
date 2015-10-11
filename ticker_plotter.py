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
from matplotlib.finance import plot_day_summary_oclh
import matplotlib.dates as dates

nslow = 26
nfast = 12
nema = 9

def plot_ticker(ticker, r, rsi, macd, ema):
    prices = r.adj_close
    dx = r.adj_close - r.close
    low = r.low + dx
    high = r.high + dx
    ma10 = talib.SMA(r.adj_close, 10)
    ma50 = talib.SMA(r.adj_close, 50)

    last = r[-1]
    volume = r.volume
    vmax = volume.max()
    
    prices = []
    for row in r:
        adj_ratio = row.adj_close/row.close
        line = dates.date2num(row.date),row.open*adj_ratio,row.close*adj_ratio,row.low*adj_ratio,row.high*adj_ratio,row.volume
        prices.append(line)

    ### plot the figure

    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)

    textsize = 9
    left, width = 0.1, 0.8
    rect1 = [left, 0.7, width, 0.2]
    rect2 = [left, 0.3, width, 0.4]
    rect3 = [left, 0.1, width, 0.2]


    fig = plt.figure(facecolor='white')
    axescolor  = '#f6f6f6'  # the axes background color

    ax1 = fig.add_axes(rect1, axisbg=axescolor)  #left, bottom, width, height
    ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
    ax2t = ax2.twinx()
    ax3  = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)

    ### plot the relative strength indicator
    fillcolor = 'darkgoldenrod'

    ax1.plot(r.date, rsi, color=fillcolor)
    ax1.axhline(70, color=fillcolor)
    ax1.axhline(30, color=fillcolor)
    ax1.fill_between(r.date, rsi, 70, where=(rsi>=70), facecolor=fillcolor, edgecolor=fillcolor)
    ax1.fill_between(r.date, rsi, 30, where=(rsi<=30), facecolor=fillcolor, edgecolor=fillcolor)
    ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
    ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=textsize)
    ax1.set_ylim(0, 100)
    ax1.set_yticks([30,70])
    ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)
    ax1.set_title('%s daily'%ticker)

    ### plot the price and volume data
    plot_day_summary_oclh(ax2, prices, colorup='#53c156', colordown='#ff1717')

    s = '%s O:%1.2f H:%1.2f L:%1.2f C:%1.2f, V:%1.1fM Chg:%+1.2f' % (
        last.date,
        last.open, last.high,
        last.low, last.close,
        last.volume*1e-6,
        last.close-last.open )
    t4 = ax2.text(0.3, 0.9, s, transform=ax2.transAxes, fontsize=textsize)

    ax2.plot(r.date, ma10, color='blue', lw=1, label='MA (10)')
    ax2.plot(r.date, ma50, color='pink', lw=1, label='MA (50)')

    props = font_manager.FontProperties(size=10)
    leg = ax2.legend(loc='upper left', shadow=True, fancybox=True, prop=props)
    leg.get_frame().set_alpha(0.5)

    poly = ax2t.fill_between(r.date, volume, 0, label='Volume', facecolor=fillcolor, edgecolor=fillcolor)
    ax2t.set_ylim(0, 5*vmax)
    ax2t.set_yticks([])



    ### plot the MACD indicator
    fillcolor = 'darkslategrey'
    ax3.plot(r.date, macd, color='blue', lw=1)
    ax3.plot(r.date, ema, color='green', lw=1)
    ax3.fill_between(r.date, macd-ema, 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)


    ax3.text(0.025, 0.95, 'MACD (%d, %d, %d)'%(nfast, nslow, nema), va='top', transform=ax3.transAxes, fontsize=textsize)

    #ax3.set_yticks([])
    # turn off upper axis tick labels, rotate the lower ones, etc
    for ax in ax1, ax2, ax2t, ax3:
        if ax!=ax3:
            for label in ax.get_xticklabels():
                label.set_visible(False)
        else:
            for label in ax.get_xticklabels():
                label.set_rotation(30)
                label.set_horizontalalignment('right')

        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')



    class MyLocator(mticker.MaxNLocator):
        def __init__(self, *args, **kwargs):
            mticker.MaxNLocator.__init__(self, *args, **kwargs)

        def __call__(self, *args, **kwargs):
            return mticker.MaxNLocator.__call__(self, *args, **kwargs)

    # at most 5 ticks, pruning the upper and lower so they don't overlap
    # with other ticks
    #ax2.yaxis.set_major_locator(mticker.MaxNLocator(5, prune='both'))
    #ax3.yaxis.set_major_locator(mticker.MaxNLocator(5, prune='both'))

    ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))
    ax3.yaxis.set_major_locator(MyLocator(5, prune='both'))

    plt.show()

#ticker='AAPL'
#DATA_DIR = 'data/'
#
#fh = open(DATA_DIR + ticker)
## a numpy record array with fields: date, open, high, low, close, volume, adj_close)
#r = mlab.csv2rec(fh)
#fh.close()
#r.sort()
#
#### compute everything
#rsi = talib.RSI(r.adj_close)
#macd, macdsignal, macdhist = talib.MACD(r.adj_close, fastperiod=nfast, slowperiod=nslow)
#ema = talib.EMA(macd, nema)
#
#plot_ticker(ticker, r, rsi, macd, ema)