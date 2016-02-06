def load_list(file_name):
    """
    load word list for given file
    """
    with open(file_name, 'rU') as file:
            word_list = [line.strip().lower() for line in file]
    return word_list



f_name = load_list('./Wordlists/femaleFirstNames.txt')
print ('Mary'.lower() in f_name)
