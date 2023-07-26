from utils.CardClass import Card
from utils.csv_utils import create_csv, append_row, sort_csv_by_column
import argparse
import re
import os
import sys

def parseText(lines, card):
    """Loops through all of the text lines passed to it and parses the text
    into a Card object.
    
    Parameters:
        lines - List of strings. 1 string = 1 text line from a file
        card - Card object that the parsed text will be entered into.
    Returns:
        card - Card object with entered parsed text.
    """
    for count, line in enumerate(lines):
        line = re.split('\n', line)[0]
        
        # Extract any API number
        api = re.search('(49)\-?\ ?0[0-9]{2}\-?\ ?([0-9]{5})\-?\ ?([0-9]{4})?', line)
        if api:
            card.api = api.group()

        # Extract the well's name/number
        wellName = re.search('NO\.\ ?.*', line)
        if wellName:
            card.well_name = re.split("NO\.\ ?" ,wellName.group())[-1]

        # Extract the well's operator
        operator = re.search('(OPERATOR|OPR)\.?\ ?.*', line)
        if operator:
            card.operator = re.split('(OPERATOR|OPR)\.?\ ?', operator.group())[-1]
        
        # Extract the township location of the well
        township = re.search('TWP\.?\ ?[0-9]{1,2}', line)
        if township:
            card.township = re.split("TWP\.?\ ?", township.group())[-1]+'N'

        # Extract the range location of the well
        range = re.search('RGE\.?\ ?[0-9]{1,3}', line)
        if range:
            card.range = re.split('RGE\.?\ ?', range.group())[-1]+'W'

        # Extract the township section of the well
        section = re.search('SEC\.?\ ?[0-9]{1,2}', line)
        if section:
            card.section = re.split('SEC\.?\ ?', section.group())[-1]

        # Extract the North line footage of the well
        NL = re.search('NL\.\ ?[0-9]+', line)
        if NL:
            card.NS_Footage = NL.group()

        # Extract the South line footage of the well
        SL = re.search('SL\.\ ?[0-9]+', line)
        if SL:
            if len(card.NS_Footage) != 0: 
                card.NS_Footage += " "
            card.NS_Footage += SL.group()

        # Extract the East line footage of the well
        EL = re.search('EL\.\ ?[0-9]+', line)
        if EL:
            card.EW_Footage = EL.group()

        # Extract the West line footage of the well
        WL = re.search('WL\.\ ?[0-9]+', line)
        if WL:
            if len(card.EW_Footage) != 0:
                card.EW_Footage+=" "
            card.EW_Footage += WL.group()

        if count < 5:
            # Extract the NSFootage of the well
            Qtr_Qtr = re.search('(C\ |C\/2\ )?((((N|E|S|W)\/2\ ?)|(NE|NW|SE|SW))\ ?){2,3}', line)
            if Qtr_Qtr:
                card.Qtr_Qtr = Qtr_Qtr.group()
        
        # Extract the elevation of the well
        elev = re.search('ELEV.*', line)
        if elev:
            card.elevation = re.split('ELEV\.?\ ?', elev.group())[-1]
        
        # Extract the spud date
        spud = re.search('COMM\.?\ ?\d{1,2}(\/|\-)\d{1,2}(\/|\-)\d{2,4}', line)
        if spud:
            card.spud = re.split('COMM\.?\ ?', spud.group())[-1]

        # Extract the completion date
        comp = re.search('COMP\.?\ ?\d{1,2}(\/|\-)\d{1,2}(\/|\-)\d{2,4}', line)
        if comp:
            card.completion = re.split('COMP\.?\ ?', comp.group())[-1]

        formation_list = [
            'SURFACE',
            'WASATCH',
            'FT. UNION',
            'LANCE',
            'FOX HILLS',
            'MESA VRD',
            'PARKMAN',
            'SHANNON',
            'EAGLE',
            'NIOBRARA',
            'FRONTIER',
            'WALL CK',
            'GR.NHORN',
            'MOWRY',
            'MUDDY',
            'N.CASTLE',
            'DAKOTA',
            'FALL RVR',
            'LAKOTA',
            'CLOVERLY',
            'MORRISON',
            'SUNDANCE',
            'CHUGWTR',
            'SPEARFISH',
            'Alcova',
            'ALCOVA',
            'EMBAR',
            'TENSLEEP',
            'MINLUSA',
            'AMSDEN',
            'MADISON',
        ]

        # Extract the Formation TD's
        for formation in formation_list:
            pattern = formation+'\.?\ *[0-9]{1,4}'
            # print(pattern)
            formationTD = re.search(pattern, line)
            if formationTD:
                card.TD_Formation+= ' ' + formationTD.group()
        
        # Extract the total depth
        TD = re.search('(T|7)\.?D\.?\ ?[0-9]{2,4}', line)
        if TD:
            card.total_depth = TD.group()
        
        # Extract the plug back
        PB = re.search('P\.?B\.?\ ?[0-9]{2,4}', line)
        if PB:
            card.plug_back = PB.group()
        
        # Extract some casing information
        casing = re.search('[0-9]{1,2}"\ ?[0-9]\/[0-9]\ ?[0-9]*', line)
        if casing:
            card.casing += ' ' + casing.group()
    
        # Extract the pool (field) location info
        pool = re.search('POOL\ ?.*', line)
        if pool:
            card.location += re.split('POOL\ ?', pool.group())[-1]

        # Extract the county location info
        county = re.search('COUNTY\ ?.*', line)
        if county:
            temp = re.split('COUNTY\ ?', county.group())[-1]
            card.location += (', ' + temp) if len(card.location) > 0 else temp

    # Set the Location
    card.setLocation()
    card.setLocationFootage()

    # Remove any possible leading spaces from sections where leading spaces
    # may be added
    card.TD_Formation = re.split("^(\ |,)*", card.TD_Formation)[-1]
    card.casing = re.split("^(\ |,)*", card.casing)[-1]
    card.location = re.split("^(\ |,)*", card.location)[-1]
    card.locationFootage = re.split("^(\ |,)*", card.locationFootage)[-1]
    
    return card


def main():
    # Parse input and output directory options
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True,
                        help="Path to directory containing text files")
    parser.add_argument("-o", "--output", required=True,
                        help="File path of CSV will be outputted to")
    args = vars(parser.parse_args())
    
    # Make sure that the output is a .csv file
    if args["output"][-4:] != '.csv':
        print("ERROR: Output file must be .csv!", file=sys.stderr)
        return

    # Create the .csv file
    create_csv(args["output"])

    # Parse all the text files in the input directory into the csv
    for filename in os.listdir(args["input"]):
        # Skip non-text files
        if not filename.endswith('.txt'):
            continue

        file = os.path.join(args["input"], filename)

        # ignore any of the checkpoint files created by jupyter
        if 'checkpoint' in file:
            continue

        card = Card()
        # Get the original name of the pdf file that the text came from
        card.documentID = os.path.basename(file)
        card.typeID = '3'
        with open(file, 'r') as text:
            lines = text.readlines()
            card = parseText(lines, card)
            # Get parsed information
            card_array = card.get_value_list()
            # Write the parsed information to the csv
            append_row(args['output'], card_array)

    # Sort the csv in ascending order by the first column
    sort_csv_by_column(args['output'], 0, True)
    print("Done")
    return

if __name__ =='__main__':
    main()