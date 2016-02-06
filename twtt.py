import csv
import sys
import NLPlib
import xml.etree.ElementTree as ET
import re
import HTMLParser


c = HTMLParser.HTMLParser()
T_RE = re.compile(r'/')   #tags and attributions
TAG_RE = re.compile(r'<[^>]+>')   #tags and attributions
URL_RE = re.compile(r'((http|https)://|www)[a-zA-Z0-9.?/&=:]*')  #url
FC_RE = re.compile(r'(@|#)+')  #first character 




#step 1

def remove_tags(text):
    """remove all html tags and attributes (/<[^>]>/)
    """
    text = T_RE.sub(' ', text)
    return TAG_RE.sub(' ', text)


#step 2
def convert_ascii(text): 
    """ Replace html character codes with ASCII equivalent
    """
    return c.unescape(text)


#step 3
def remove_url(text):
    """ Remove all URLs 
    """
    return URL_RE.sub('', text)

    
#step 4
def remove_first_cha(text):
    """ Remove Twitter usernme @ and hash tags #
    """
    return FC_RE.sub('', text)


#step 5
def find_end(text):
    """ Finding end of sentences based on the instruction of 4.2.4.
    of the Manning and Schutze text. replace end of sentence # with #/#
    at end of each sentence """
    
    #place putative sentence boundaries after all occurrenceof .?!;:-
    text = text.replace(".", "./.")
    text = text.replace("?", "?/?")
    text = text.replace("!", "!/!") #problem: what about !!!
    text = text.replace(";", ";/;")
    text = text.replace(":", ":/:")

    print "after replace symbols" + text
    print "\n"

    #move the boundary after following quotation marks, if any
    text = text.replace('"', "")

      
    word_list = text.split(" ")# split text
    print "after split"+str(word_list)
    print "\n"

    length = len(word_list) # measure length of word list in advance b/c we wanna use it many time
    for j in range(0,length):
        #Disqualify a period boundary in the following circumstances
        if ("./." == word_list[j][-3:]):
            #preceded by a known abbr. and followed by a capitalized name
            if ((word_list[j][:-2]).lower() in abbr) and (j<length-1):# and (word_list[j+1] in names):
                print "case 1.1"
                word_list[j] = word_list[j][:-3] + "."   #replace ./. by .

            #if preceded by a known abbr and followed by lowercase.
            elif (word_list[j][:-2].lower() in abbr) and word_list[j+1][0].islower() and (j<length-1):
                print "case 1.2"
                word_list[j] = word_list[j][:-3] + "."   #replace ./. by .

        # Disqualify a boundary with a ? or ! if:
        if ("?/?" == word_list[j][-3:] or "!/!" == word_list[j][-3:]):
            print "case 2"
            # if followed by a name or lowercase letter.
            if ((word_list[j+1][0].islower()) or (word_list[j+1].lower() in names) and (j<length-1)):
                word_list[j] = word_list[j][:-3] +  word_list[j][-1]  #replace ?/? by ? or replace !/! by !
          
    return word_list


def lists():
    """
    abbr = load_list('/u/cs401/Wordlists/abbrev.english')
    pn_abbr = load_list('/u/cs401/Wordlists/pn_abbrev.english')
    m_name = load_list('/u/cs401/Wordlists/maleFirstNames.txt')
    f_name = load_list('/u/cs401/Wordlists/femaleFirstNames.txt')
    last_name = load_list('/u/cs401/Wordlists/lastNames.txt')
    """
    #global abbr, name, pn_abbr
  
    

def load_list(file_name):
    """
    load word list for given file
    """
    with open(file_name, 'rU') as file:
            word_list = [line.strip().lower() for line in file]
    return word_list

    
#step6-9
def tweet_tag(sentence):
    tagger = NLPlib.NLPlib()
    tokenized = tagger.tokenize(sentence)
    tags = tagger.tag(sentence)
    for i in range(len(tokenized)):
        tokenized[i] += tags[i] 
    return sentence

if __name__ == '__main__':
    
    #check the validity of the input argument
    if len(sys.argv) == 4:
        test_data_set = range(5500*sys.argv[2], 5500*sys.argv[2]-1)
    
    abbrrev = load_list('./Wordlists/abbrev.english')
    pn_abbr = load_list('./Wordlists/pn_abbrev.english')
    m_name = load_list('./Wordlists/maleFirstNames.txt')
    f_name = load_list('./Wordlists/femaleFirstNames.txt')
    last_name = load_list('./Wordlists/lastNames.txt')    
    names = m_name + f_name + last_name
    abbr = abbrrev + pn_abbr      
    
    with open(sys.argv[1], 'rb') as csvfile:
        reader = csv.reader(csvfile)   # opens the csv file
        output_file = open(sys.argv[2], 'wb')
        
        for line in reader:   # iterates the rows of the file in orders
            if line in test_data_set:
                #The reader function will take each line of the file and make a list containing all that line's columns. 
                output_file.write('<A=' + line[0] + '>')
                #Only keep the tweet, discard tweet time and usrname 
                tweet = line[-1]
                tweet = remove_url(tweet)
                tweet = remove_tags(tweet)
                tweet = convert_ascii(tweet)
                tweet = remove_first_cha(tweet)
                tweet = find_end(tweet)
                tweet = tweet_tag(tweet)

    input_file.close() 
    output_file.close()
