import pandas as pd
import numpy as np
import math
from dateutil.parser import parse
from optparse import OptionParser

def fledger(account,amount,asset,balance=float("NaN")):
    if asset == "ZEUR":
        asset = "EUR";
    if asset == "ZUSD":
        asset = "USD";
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
            if subframe.iloc[0]['fee'] == 0:
                fledger(options.krakenaccount,subframe.iloc[0]['amount'],subframe.iloc[0]['asset'],subframe.iloc[0]['balance'],)
#                print("\t",options.krakenaccount,"\t\t",subframe.iloc[0]['asset'],np.format_float_positional(subframe.iloc[0]['amount'],trim='-'))
            else:
#                fledger(options.krakenaccount,subframe.iloc[0]['asset'],np.format_float_positional(subframe.iloc[0]['balance']
                print("\t",options.krakenaccount,"\t=",subframe.iloc[0]['asset'],np.format_float_positional(subframe.iloc[0]['balance'],trim='-'))
            if subframe.iloc[1]['fee'] == 0:
                print("\t",options.krakenaccount,"\t\t",subframe.iloc[1]['asset'],np.format_float_positional(subframe.iloc[1]['amount'],trim='-'))
            else:
                print("\t",options.krakenaccount,"\t=",subframe.iloc[1]['asset'],np.format_float_positional(subframe.iloc[1]['balance'],trim='-'))
            print("\t",options.feeaccount,"\t\t",subframe.iloc[0]['asset']," ",np.format_float_positional(subframe.iloc[0]['fee'],trim='-'))
            print("\t",options.feeaccount,"\t\t",subframe.iloc[1]['asset']," ",np.format_float_positional(subframe.iloc[1]['fee'],trim='-'))

    elif isinstance(row['txid'],str):
#        print(type(row['txid']))
        print(date.strftime('%Y/%m/%d'),"* ",row['type'])
        for index, value in row.items():
            print("\t; ",index,": ",value)
        print("\t",options.krakenaccount,"\t=",row['asset'],np.format_float_positional(row['balance'],trim='-'))
        print("\t",options.feeaccount,"\t\t",row['asset']," ",np.format_float_positional(row['fee'],trim='-'))

        if row['type']=='deposit':
            print("\t",options.externalaccount,"\t\t",row['asset'],np.format_float_positional(-row['amount'],trim='-'))
        if row['type']=='transfer':
            print("\t",options.transferaccount,"\t\t",row['asset'],np.format_float_positional(-row['amount'],trim='-'))
        if row['type']=='withdrawal':
            print("\t",options.externalaccount,"\t\t",row['asset'],np.format_float_positional(-row['amount'],trim='-'))


