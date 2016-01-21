import csv
import sys
#import NLPlib


#step 1-5
def tweet_tokenize():
    return

#step6-9
def tweet_tag():
    tagger = NLPlib.NLPlib()
    
    return

if __name__ == '__main__':
    
    input_file = open(sys.argv[2], 'rb') # opens the csv file
    try:
        outputfile = open(sys.argv[4], 'wb')
        reader = csv.reader(file)  # creates the reader object
        for row in reader:   # iterates the rows of the file in orders
            
            #The reader function will take each line of the file and make a list containing all that line's columns. 
            
            #todo
            tweet_tokenize(row)
            tweet_tag(row)
    finally:
        
        input_file.close() 
        output_file.close()