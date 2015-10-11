import xml.etree.ElementTree
import urllib2

sp500_list_url='http://www.cboe.com/products/snp500.aspx'

def download_symbol_list():
    symbols_filename='symbols'
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

print len(download_symbol_list())