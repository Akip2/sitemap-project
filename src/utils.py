def treat_str_input(input):
    if(input == None or len(input) == 0):
        return None
    else:
        return input
    
def treat_int_input(input, min=1):
    if(input == None):
        return None
    
    converted = int(input)
    try:
        if(converted > min):
            return converted
        else:
            return min
    except:
        return None

def trear_array_input(input):
    if(input == None or len(input) == 0):
        return None
    else:
        array = input.split(",")
        return array