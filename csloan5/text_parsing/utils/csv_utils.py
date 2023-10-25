import csv
import os
import glob
import shutil
import pandas as pd

#all functions
def ocr_status(csv_file, CardTypeID, status):
    rows = []
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    for row in rows:
        if row['CardTypeID'] == CardTypeID:
            row['Status'] = status

    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
def sort_csv_by_column(csv_file, sort_column, ascend):
    
    df = pd.read_csv(csv_file)  # Read the CSV file into a DataFrame
    df.sort_values([df.columns[sort_column]], axis=0, ascending=[ascend], inplace=True)  # Sort DataFrame by the chosen column
    
    # Write sorted data back to the CSV file
    df.to_csv(csv_file, index=False)

    
def compare_and_print(csv_file, lst):
    with open(csv_file, 'r', newline='') as file:
        rows = list(csv.reader(file))

    for row in rows:
        if row[0] == str(lst[0]):
            row[3:] = lst[1:]  # Update from column 4 onwards

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        
def compare_and_print_multi(csv_file, list_of_lists):
    with open(csv_file, 'r', newline='') as file:
        rows = list(csv.reader(file))

    for lst in list_of_lists:
        for row in rows:
            if row[0] == str(lst[0]):
                row[3:] = lst[1:]  # Update from column 4 onwards
                break  # Break the inner loop if match found for efficiency

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        

def delete_rows(csv_file, start_row, end_row):
    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Delete the specified range of rows
    if start_row < len(rows):
        del rows[start_row:end_row+1]

    # Write the updated rows back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        

def get_file_names(folder_path):
    file_names = []
    for file_path in glob.glob(os.path.join(folder_path, '*')):
        if os.path.isfile(file_path):
            file_names.append(os.path.basename(file_path))
    return file_names


def write_row(csv_file, array):
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(array)

def append_row(csv_file, array):
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(array)
        
        
def write_column(csv_file, array):
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in array:
            writer.writerow([item])
        

def append_column(csv_file, array, Offset, Card_Type_ID):
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in array:
            writer.writerow([None]*Offset+ [item]+ [Card_Type_ID])

def create_csv(csv_file):
    header = ['DocumentID','CardTypeID','OCRStatus','APINum','WellName',
        'Operator','Location','Township','Range','Section',
        'NSFootage','EWFootage','QtrQtr','LocationFootage','Elevation',
        'SpudDate','CompDate','TDFormation','TotalDepth','PlugBackDepth',
        'Casing','InitProd','ProdZone','CardNumber','WellStatus','Reeissued',
        'DSTS_Cores']

    ###format file and print headder
    if not os.path.exists(csv_file):
        with open(csv_file, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header)