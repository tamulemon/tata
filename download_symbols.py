import xml.etree.ElementTree
import urllib2
import shutil
import datetime
import matplotlib.finance as finance
import os
import time 

data_folder='data'
if not os.path.isdir(data_folder):
    os.mkdir(data_folder)

def download_ticker_data(ticker):
    fullpath = data_folder + '/' + ticker
    today = enddate = datetime.date.today()
    startdate = enddate - datetime.timedelta(days=180)
    try:
        fh = finance.fetch_historical_yahoo(ticker, startdate, enddate)
        shutil.copy2(fh.name, fullpath)
        fh.close()
        return True, None
    except Exception, e:
        return False,str(e)

def download_sp500_list():
    sp500_list_url='http://www.cboe.com/products/snp500.aspx'
    try:
        raw_source = urllib2.urlopen(sp500_list_url).read()
        split_source = raw_source.split('\n')
        filtered_source = '<symbols>'
        for line in split_source:
            if '<td>' in line and '</td>' in line:
                filtered_source = filtered_source + line.strip()
        filtered_source = filtered_source + '</symbols>'
        
        root = xml.etree.ElementTree.fromstring(filtered_source)
        
        symbols = []
        for symbol in root.iter('td'):
            symbols.append(symbol.text)
        return symbols
    except Exception, e:
        print str(e), 'failed to pull/parse data.'

def download_sp400_list():
    sp400_list_url = 'http://www.barchart.com/stocks/sp400.php?_dtp1=0'
    try:
        raw_source = urllib2.urlopen(sp400_list_url).read()
        split_source = raw_source.split('\n')
        for line in split_source:
            if '<input type="hidden" name="symbols" value="' in line:
                filtered_source = line.replace('<input type="hidden" name="symbols" value="','').replace('" />','').strip()
        symbols = []
        for symbol in filtered_source.split(','):
            if symbol != '':
                symbols.append(symbol)
        return symbols
    except Exception, e:
        print str(e), 'failed to pull/parse data.'
        
#def download_symbol_list():
#    symbol_list_url='http://www.batstrading.com/market_data/symbol_listing/xml/'
#
#    symbols_filename='symbols'
#    try:
#        symbols_xml = urllib2.urlopen(symbol_list_url).read()
#        root = xml.etree.ElementTree.fromstring(symbols_xml)
#        symbols = []
#        for symbol in root.iter('symbol'):
#            symbols.append(symbol.get('name'))
#        return symbols
#    except Exception, e:
#        print str(e), 'failed to pull/parse data.'

class State:
    SUCCESS_LABEL='success'
    
    def __init__(self):
        self.counters = {}    
    def succeeded(self):
        if self.SUCCESS_LABEL in self.counters:
            self.counters[self.SUCCESS_LABEL] = self.counters[self.SUCCESS_LABEL] + 1
        else:
            self.counters[self.SUCCESS_LABEL] = 1

    def failed(self, error):
        if error in self.counters:
            self.counters[error] = self.counters[error] + 1
        else:
            self.counters[error] = 1
    
    def get(self):
        return self.counters

symbol_list = download_sp400_list() + download_sp500_list()

state = State()

for ticker in symbol_list:
    print 'downloading ticker',ticker
    success, error = download_ticker_data(ticker)
    
    if success:
        state.succeeded()
    else:
        state.failed(error)
        
    print state.get()
    time.sleep(10)
