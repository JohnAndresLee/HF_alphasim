def create_set(input_str):
    # Split the input string by spaces to get the elements
    elements = input_str.split()
    # Create a set from the elements
    custom_set = {}
    for element in elements:
        custom_set[element] = True
    return custom_set

def intersection(set1, set2):
    # Find the intersection of two sets
    common_elements = {}
    for element in set1:
        if element in set2:
            common_elements[element] = True
    return common_elements

def sort_alphanumeric(values):
    # Sort values alphanumerically
    return sorted(values, key=lambda x: (x.isdigit(), x))

def display_results(common_elements):
    if common_elements:
        sorted_elements = sort_alphanumeric(common_elements.keys())
        print(" ".join(sorted_elements))
    else:
        print("NULL")

def main():
    # Read two lines of input
    set1_str = input("Enter the first set of values: ")
    set2_str = input("Enter the second set of values: ")
    
    # Create sets from input strings
    set1 = create_set(set1_str)
    set2 = create_set(set2_str)
    
    # Find common elements
    common_elements = intersection(set1, set2)
    
    # Display results
    display_results(common_elements)
