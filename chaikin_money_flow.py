import matplotlib.mlab as mlab
import numpy as np

# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:chaikin_money_flow_cmf
#
#  1. Money Flow Multiplier = [(Close  -  Low) - (High - Close)] /(High - Low) 
#
#  2. Money Flow Volume = Money Flow Multiplier x Volume for the Period
#
#  3. 20-period CMF = 20-period Sum of Money Flow Volume / 20 period Sum of Volume 
		
def CMF(r, timeperiod):
    mf_multiplier = ((r.close-r.low) - (r.high-r.close))/(r.high-r.low)
    mf_volume = mf_multiplier * r.volume
    cmf = []
    for i in range(len(r)):
        
        if i<timeperiod-1:
            cmf.append(np.nan)
        else:
            cmf.append(sum(mf_volume[i-timeperiod+1:i+1])/sum(r.volume[i-timeperiod+1:i+1]))
            
    return cmf

#fh = open('data/AAL')
## a numpy record array with fields: date, open, high, low, close, volume, adj_close)
#r = mlab.csv2rec(fh)
#r.sort()
#print CMF(r, 20)