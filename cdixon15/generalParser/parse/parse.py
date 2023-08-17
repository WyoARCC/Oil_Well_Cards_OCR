def left_is_close(list1, list2, dist):
    # Make the list elements numerical so numerical comparisons will be easier
    list1 = list(map(transform_element, list1))
    list2 = list(map(transform_element, list2))
    
    # First determine the leftmost text out of the two, then use that to 
    # check if the words should be joined together.
    if list1[6] < list2[6]:
        return (abs((list1[6] + list1[8]) - list2[6]) <= dist)
    else: 
        return (abs((list2[6] + list2[8]) - list1[6]) <= dist)
    
def top_is_close(line1, line2, dist):
    # Determine if the top coordinates of the two lines are within dist of
    # each other
    return (abs((int(line1[7]) + int(line1[9])) - 
                (int(line2[7]) + int(line2[9]))) <= dist)

def transform_element(item):
    # Attempts to change the item's to a float. If that doesn't work then the
    # item is returned as is. If it does work, then it will then either return
    # the float or change the float to an int and return that if possible.
    try:
        num = float(item)
    except (TypeError, ValueError):
        return item
    else:
        if num.is_integer():
            return int(num)
        else:
            return num


def combine_lines(list1, list2):
    # First convert all of the numerical strings in the list to either ints
    # or floats, and leave the text as a string.
    list1 = list(map(transform_element, list1))
    list2 = list(map(transform_element, list2))

    # Calculate the new coordinate information for combined text
    left = min(list1[6], list2[6])
    top = min(list1[7], list2[7])
    height = max(list1[9], list2[9])
    conf = ((list1[10] / 100) * (list2[10]/ 100)) * 100
    
    # Ensure that the lists can be passed to this function in any order
    if left == list1[6]:
        width = abs((list2[6] + list2[8]) - list1[6])
        text = f'{list1[11]} {list2[11]}'
    else:
        width = abs((list1[6] + list1[8]) - list2[6])
        text = f'{list2[11]} {list1[11]}'
    
    # Change the elements of the new list to all strings again, and return
    combined_list = list1[:6].copy()
    combined_list.extend([left, top, width, height, conf, text])
    combined_list = list(map(str, combined_list))
    return combined_list
    
def realign_text(text_rows, left_dist_def, top_dist_def):
    # Create a copy of the line so we can iterate without changing the iterable
    realigned = text_rows.copy()
    # Keep track of whether or not any changes are made
    has_been_modified = False 
    # Compare every row to every other row only once. Do not compare a row to
    # itself
    for index, item1 in enumerate(text_rows):
        for item2 in text_rows[index+1:]:
#########################################  Mesaverde Example  #########################################
            if re.search('Mesaverde', item1[11]):
                left_dist = left_dist_def+60
            else:
                left_dist = left_dist_def
            
            top_dist = top_dist_def
            # Check if the two rows being compared are 'close'
            if top_is_close(item1, item2, top_dist) and left_is_close(item1, item2, left_dist):
                # The realigned list is going to become shorter, so we need to
                # ensure that the item we are comparing is still in the
                # realigned list.
                try:
                    # Get the positions of the two lines of text that will be
                    # combined
                    first_pos = realigned.index(item1)
                    second_pos = realigned.index(item2)
                except ValueError:
                    # One of the lines was removed
                    continue

                # Ensure that we combine the text in the right order
                if int(item1[6]) < int(item2[6]):
                    realigned[first_pos] = combine_lines(item1, item2)
                    realigned.pop(second_pos)
                else:
                    realigned[second_pos] = combine_lines(item1, item2)
                    realigned.pop(first_pos)
                    
                has_been_modified = True # Changes have been made
    return has_been_modified, realigned
