import pandas as pd
import numpy as np
import math
from dateutil.parser import parse
from optparse import OptionParser

def fledger(account,amount,asset,balance=float("NaN")):
    amount = round(amount,10)
    if asset == "ZEUR":
        asset = "EUR";
        amount = round(amount,2)
        balance = round(balance,2)
    if asset == "ZUSD":
        asset = "USD";
        amount  = round(amount,2)
        balance = round(balance,2)
    ll="  "+account+"  "+asset+" "
    if options.decimalcomma:
        ll=ll+np.format_float_positional(amount,trim='-').replace(".",",")
    else: 
        ll=ll+np.format_float_positional(amount,trim='-')
    if not math.isnan(balance):
        ll=ll+" = "+asset+" "
        if options.decimalcomma:
            ll=ll+np.format_float_positional(balance,trim='-').replace(".",",")
        else:
            ll=ll+np.format_float_positional(balance,trim='-')
    print(ll)
#    print("\t",options.krakenaccount,"\t\t",subframe.iloc[0]['asset'],np.format_float_positional(subframe.iloc[0]['amount'],trim='-'))

parser = OptionParser()
parser.add_option("-i", "--infile", dest="infile",
                  help="csv file to import", metavar="FILE")
parser.add_option("-k", "--krakenaccount", dest="krakenaccount",
                  help="Name of the Kraken accoutn", default="Kraken")
parser.add_option("-e", "--externalaccount", dest="externalaccount",
                  help="Name of the external account", default="External")
parser.add_option("-f", "--feeaccount", dest="feeaccount",
                  help="Name of the fee account", default="Fee")
parser.add_option("-t", "--transferaccount", dest="transferaccount",
                  help="Name of the transfer account", default="Holdingwallet")
parser.add_option("-d", "--decimal-comma",
                  action="store_true", dest="decimalcomma", default=False,
                  help="use decimal comma for ledger output")

(options, args) = parser.parse_args()

trade_refids=[]
df = pd.read_csv(options.infile)
#print(df)n

for index, row in df.iterrows():
#    print(row)
    date=parse(row['time'])
    if row['type']=='trade':
        if row['refid'] not in trade_refids:
            trade_refids.append(row['refid'])
            subframe=df.loc[df['refid'] == row['refid']]
            date=parse(subframe.iloc[0]['time'])
            print(date.strftime('%Y/%m/%d'),"* Trade")
            for index, value in subframe.iloc[0].items() :
                print("\t; ",index,": ",value)
            for index, value in subframe.iloc[1].items() :
                print("\t; ",index,": ",value)
            fledger(options.krakenaccount,subframe.iloc[0]['amount']-subframe.iloc[0]['fee'],subframe.iloc[0]['asset'],subframe.iloc[0]['balance'])
            fledger(options.krakenaccount,subframe.iloc[1]['amount']-subframe.iloc[1]['fee'],subframe.iloc[1]['asset'],subframe.iloc[1]['balance'])
            fledger(options.feeaccount,subframe.iloc[0]['fee'],subframe.iloc[0]['asset'])
            fledger(options.feeaccount,subframe.iloc[1]['fee'],subframe.iloc[1]['asset'])

    elif isinstance(row['txid'],str):
#        print(type(row['txid']))
        print(date.strftime('%Y/%m/%d'),"* ",row['type'])
        for index, value in row.items():
            print("\t; ",index,": ",value)
        fledger(options.krakenaccount,row['amount']-row['fee'],row['asset'],row['balance'])
        fledger(options.feeaccount,row['fee'],row['asset'])
        if row['type']=='deposit':
            fledger(options.externalaccount,-row['amount'],row['asset'])
        if row['type']=='transfer':
            fledger(options.transferaccount,-row['amount'],row['asset'])
        if row['type']=='withdrawal':
            fledger(options.externalaccount,-row['amount'],row['asset'])



