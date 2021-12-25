import pandas as pd
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--infile", dest="infile",
                  help="csv file to import", metavar="FILE")

(options, args) = parser.parse_args()

print("")
df = pd.read_csv(options.infile)
print(df)
