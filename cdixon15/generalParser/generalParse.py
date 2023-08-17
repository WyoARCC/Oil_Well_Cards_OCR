import pandas
import os
import argparse
import glob

import tsvcsv.tsvcsv as tb

#TODO parses an indivudal TSV and outputs a corresponding data frame row
def parseTSV(tsv):
    dfI=tb.loadTSV(tsv)

    #this is the default value newrow. each value is just '**NOTFOUND**'
    parsed=tb.defaultRow

    '''
    Call some parser functions and edit values in 'parsed' accordingly
    '''
    
    return parsed

#Recursively or non recursively parses a directory of tsv files and places the results in one data frame
def parseDirectory(directory,recursive=False):
    dfOut=tb.dfInit()    
    files = glob.glob(directory + '/**/*.tsv', recursive=recursive)
    for file in files:
        print(file)
        parsed=parseTSV(file)
        dfOut.loc[len(dfOut.index)] = parsed

    return dfOut



#TODO 
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
    	help="path to input pdf file")     
    ap.add_argument("-o", "--output", required=True,
        help="path to output file") 
    ap.add_argument("-r", "--recursive", required=False,
        help="bool determining if a parseDirectory job is recursive or not") 
    args = vars(ap.parse_args())

    if os.path.isdir(args['input']):
        df=parseDirectory(args["input"],args['recursive'])
        df.to_csv(args['output'])
        print(parseDirectory(args["input"],args['recursive']))

    else:
        parseTSV(args["input"])
   
    
    
    
    return

if __name__ =='__main__':    
    main()