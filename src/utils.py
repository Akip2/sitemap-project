def treat_str_input(input):
    if(input == None or len(input) == 0):
        return None
    else:
        return input
    
def treat_int_input(input, min=1):
    if(input == None):
        return None
    elif(input < min):
        return min
    else:
        return input

def trear_array_input(input):
    if(input == None or len(input) == 0):
        return None
    else:
        array = input.split(",")
        return array