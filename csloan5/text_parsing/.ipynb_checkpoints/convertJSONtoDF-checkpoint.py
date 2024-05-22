import json
import pandas as pd

def convert_JSON_to_df(filename):
    """Takes a file path string to a JSON file outputted by Cloud Vision and
    converts that JSON to a Pandas Dataframe.
    
    Parameters:
        filename: String of the location of the JSON file.
    Returns:
        df: A pandas dataframe containing relevant information from the JSON
        files
    """
    
    # Opening JSON file and store it in dictionary
    with open(filename) as f:
        data = json.load(f)
    # Create new dataframe and set the header
    df = pd.DataFrame(columns=[
        'level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num',
        'left', 'top', 'width', 'height', 'conf', 'text'
    ])

    # Loop through the dictionary and extract text data and positional data
    for i in range(1, len(data['textAnnotations'])):
        text = data['textAnnotations'][i]['description']
        conf = data['textAnnotations'][i]['confidence']
        top_l = data['textAnnotations'][i]['boundingPoly']['vertices'][0]
        top_r = data['textAnnotations'][i]['boundingPoly']['vertices'][1]
        bottom_r = data['textAnnotations'][i]['boundingPoly']['vertices'][2]
        bottom_l = data['textAnnotations'][i]['boundingPoly']['vertices'][3]
        # Use bounding box vertices to calculate the left-most and top-most 
        # coordinate of each word, and the width and height of the words
        left = min(top_l['x'], bottom_l['x'])
        right = max(top_r['x'], bottom_r['x'])
        top = min(top_l['y'], top_r['y'])
        bottom = max(bottom_l['y'], bottom_r['y'])
        width = right - left
        height = bottom - top
        # Add the information to the dataframe
        df.loc[len(df.index)] = ['json', '1', '0', '0', '0', '0', left, top, width, height, conf, text]
    return df
