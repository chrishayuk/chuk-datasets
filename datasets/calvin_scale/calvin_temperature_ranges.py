def get_calvin_temperature_ranges():
    return {
        "You've taken that too far": (float('-inf'), -2.0),
        "Bloomin' Freezin'": (-2, 0.0),
        "Freezin'": (0.0, 1.0),
        "Bloomin' Cold": (1.0, 2.0),
        "A bit Cold": (2.0, 3.0),
        "A wee bit nippy": (3.0, 4.0),
        "Alright": (4.0, 5.0),
        "Getting a bit Lovely": (5.0, 6.0),
        "Lovely": (6.0, 7.0),
        "Nice and Warm": (7.0, 8.0),
        "Getting a bit Hot": (8.0, 9.0),
        "Hot": (9.0, 10.0),
        "Toasty": (10.0, 11.0),
        "Roasty Toasty": (11.0, 12.0),
        "Ridiculous": (12.0, float('inf'))
    }

def get_calvin_scale_classification(calvin):
    # get the calvin temperature ranges
    temperature_ranges = get_calvin_temperature_ranges()
    
    # check and return the classification
    for classification, (lower_bound, upper_bound) in temperature_ranges.items():
        if lower_bound <= calvin < upper_bound:
            return classification
        
    # not needed, but returned as a fail safe
    return "Haveny got a clue"

def get_lowest_calvin_scale_number():
    # get the temperature ranges
    temperature_ranges = get_calvin_temperature_ranges()

    # Initialize variable to store the minimum value, starting with a high value that will definitely be overridden.
    min_value = float('inf')

    # Loop through each classification range
    for _, (lower_bound, _) in temperature_ranges.items():
        if lower_bound != float('-inf') and lower_bound < min_value:
            min_value = lower_bound
    
    # return the min value
    return min_value

def get_highest_calvin_scale_number():
    # get the temperature ranges
    temperature_ranges = get_calvin_temperature_ranges()

    # Initialize variable to store the maximum value, starting from a very low value.
    max_value = float('-inf')
    
    # Loop through each classification range
    for _, (_, upper_bound) in temperature_ranges.items():
        if upper_bound != float('inf') and upper_bound > max_value:
            max_value = upper_bound
    return max_value
