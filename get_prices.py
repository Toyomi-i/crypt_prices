from pycoingecko import CoinGeckoAPI
import datetime
import pandas as pd
import os

# transfer timestamp to date 
def get_price(r2):
    s = pd.DataFrame(r2['prices'])
    s.columns = ['date', 'ATOMprice_jpy']
    date = []
    for i in s['date']:
        tsdate = int(i / 1000)
        loc = datetime.datetime.utcfromtimestamp(tsdate)
        date.append(loc)
    s.index = date
    del s['date']
    return s

# get lastmonth using default library of AWS lambda
def get_lastmonth():
    today       = datetime.datetime.today()
    thismonth   = datetime.datetime(today.year, today.month, 1)
    lastmonth   = thismonth + datetime.timedelta(days=-1)
    return lastmonth

# Main
os.chdir('/Users/toyomiishida/Documents/personal')
cg = CoinGeckoAPI()

# get cosmos prices
r2 = cg.get_coin_market_chart_by_id(
    id          = 'cosmos', 
    vs_currency = 'jpy', 
    days        = 'max'
)
atmprices = get_price(r2)

# extract lastmonth data
lastmonth = get_lastmonth()
lastmonth_flags = (atmprices.index.month == lastmonth.month) \
                  & (atmprices.index.year == lastmonth.year)

# export as csv
atmprices[lastmonth_flags].to_csv('prices_file/' + lastmonth.strftime('%Y_%m') + '_atmprices.csv')