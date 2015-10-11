import urllib2

sp400_list_url = 'http://www.barchart.com/stocks/sp400.php?_dtp1=0'

def download_symbol_list():
    symbols_filename='symbols'
    try:
        raw_source = urllib2.urlopen(sp400_list_url).read()
        split_source = raw_source.split('\n')
        for line in split_source:
            if '<input type="hidden" name="symbols" value="' in line:
                filtered_source = line.replace('<input type="hidden" name="symbols" value="','').replace('" />','')
        filtered_source = filtered_source.strip()
        symbols = []
        for symbol in filtered_source.split(','):
            if symbol != '':
                symbols.append(symbol)
        return symbols
    except Exception, e:
        print str(e), 'failed to pull/parse data.'

print download_symbol_list()