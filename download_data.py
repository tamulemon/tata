import xml.etree.ElementTree


    root = xml.etree.ElementTree.fromstring(symbols_xml)
    symbols = []
    for symbol in root.iter('symbol'):
        symbols.append(symbol.get('name'))