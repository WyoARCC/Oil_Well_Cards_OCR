import pandas

#TODO searches a tsv for lines which potentially match a certain field
'''
tsv=the tsv to use as loaded by loadTSV
fieldDict=the tect file to use as a dictionary of potential field names. For example, section may be represented as 
    'section' 'sect.' 'sec.' or in some other way
'''
def fieldSearch(tsv,fieldDict):
    
    return

#Loads the tsv at tsvPATH as a pandas data frame and returns that data frame
def loadTSV(tsvPATH):
    csv = pandas.read_csv(tsvPATH, sep='\t')
    return csv

#TODO initializes a pandas data frame to hold final parsed values
def dfInit():
    df=pandas.DataFrame(columns=['FileNum','CardTypeID','Status','DocumentID','APINum','WellName',
     'Operator','Location','Township','Range','Section',
     'NSFootage','EWFootage','QtrQtr','LocationFootage',
     'Elevation','SpudDate','CompDate','TDFormation','TotalDepth',
     'PlugBackDepth','Casing','InitProd','ProdZone',',CardNumber','Status','Reeissued','DSTS_Cores'])    
    return df

defaultRow={'FileNum':'**NOTFOUND**',
            'CardTypeID':'**NOTFOUND**',
            'Status':'**NOTFOUND**',
            'DocumentID':'**NOTFOUND**',
            'APINum':'**NOTFOUND**',
            'WellName':'**NOTFOUND**',
            'Operator':'**NOTFOUND**',
            'Location':'**NOTFOUND**',
            'Township':'**NOTFOUND**',
            'Range':'**NOTFOUND**',
            'Section':'**NOTFOUND**',
            'NSFootage':'**NOTFOUND**',
            'EWFootage':'**NOTFOUND**',
            'QtrQtr':'**NOTFOUND**',
            'LocationFootage':'**NOTFOUND**',
            'Elevation':'**NOTFOUND**',
            'SpudDate':'**NOTFOUND**',
            'CompDate':'**NOTFOUND**',
            'TDFormation':'**NOTFOUND**',
            'TotalDepth':'**NOTFOUND**',
            'PlugBackDepth':'**NOTFOUND**',
            'Casing':'**NOTFOUND**',
            'InitProd':'**NOTFOUND**',
            'ProdZone':'**NOTFOUND**',
            ',CardNumber':'**NOTFOUND**',
            'Status':'**NOTFOUND**',
            'Reeissued':'**NOTFOUND**',
            'DSTS_Cores':'**NOTFOUND**',}