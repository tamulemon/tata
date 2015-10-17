# Technical Analysis Based Stock Scanner

## Prerequisite
* install TA-Lib http://mrjbq7.github.io/ta-lib/doc_index.html
<pre>
brew install TA-Lib
pip install TA-Lib
</pre>
* install matplotlib http://matplotlib.org/
<pre>
pip install matplotlib
</pre>

## Download tickers
Download tickers from yahoo finanace chart API service:
<pre>
python download_tickers.py
</pre>

## Run Scanner
Run following script to scan dowloaded tickers
<pre>
python simple_scanner.py
</pre>

## View Scan Result
Run following command and open up http://localhost:8000 in any browser:
<pre>
python -m SimpleHTTPServer
</pre>


