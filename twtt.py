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
P_RE = re.compile(r'\.\.\.\.+') # more than 3 periods


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
    try:
        text = c.unescape(text)
    except:
        text = ""
    return text


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
    at end of each sentence. Return a list of conponents sentence """

    # transfer more than 3 excalmatory marks to !!!
    text = P_RE.sub("...", text)
    
    #move the boundary after following quotation marks, if any
    text = text.replace('"', "")
    word_list = (text.strip()).split()# split text
    
    length = len(word_list) # measure length of word list in advance b/c we wanna use it many time
    for j in range(0,length):
        #Add end of sentenct mark for following situation

        # ecllipsis
        if (".." == word_list[j][-2:]):
            word_list[j] += " "
            
        #case 2: period
        elif (j<length-1 and "." == word_list[j][-1]):
            ps = re.search(r"[a-zA-Z]+", word_list[j+1])
            if ps:
                if not (((word_list[j]).lower() in abbr) and (((ps.group()).lower() in names) or (ps.group()[0].islower()))):
                        word_list[j] += "\n"
                else:
                    word_list[j] += " "
                    

        # case 3: ! and ?
        elif (j<length-1 and ("?" == word_list[j][-1] or "!" == word_list[j][-1])):
            if word_list[j+1].isalpha():
                ps = re.search(r"[a-zA-Z]+", word_list[j+1])
                if ps:
                    if not (((ps.group()).lower() in names) or (ps.group()[0].islower())):
                        word_list[j] += "\n"
                    else:
                        word_list[j] += " "
            else:
                word_list[j] += "\n"
        # case 4: non-special word
        else:
            word_list[j] += " "
                
    return ("".join(word_list)).split("\n")
          

def load_list(file_name):
    """
    load word list for given file
    """
    with open(file_name, 'rU') as file:
            word_list = [line.strip().lower() for line in file]
    return word_list

    
#step6-9
def EOS_split(sentence):
    """
    help split end of sentence punctuation from the word
    """
    splitted = sentence[:-1] + filter(None, re.split(r'([a-zA-Z]+)', sentence[-1]))
    return splitted

def split_token(token):
    if not token.strip():
        return list(token)    
    token = [" ".join(token.split()[:-1]), token.split()[-1]]
    #print(token)
    token = filter(None, re.split(r'(,)(?=[\D])|(\!)|(\.\.\.)|(\?)|(\#)|(\@)|(\$)|(\")|(\'s)|(\')|(n\'t)|(\s)', token[0])) + \
            filter(None, re.split(r'(\!)|(\.\.\.)|(\?)|(\#)|(\@)|(\$)|(\,\s)|(\")|(\'s)|(\')|(n\'t)|(\.)|(\s)', token[1]))
    
    return filter(lambda a: a != ' ', token)

def my_split(token):
    return filter(None, re.split(r'(,)(?=[\S])', token))
                  
def tweet_tag(sentence):
    print("tweet tag   ---->> ", sentence)
    sentence = split_token(sentence)
    tags = tagger.tag(sentence)
    for i in range(len(sentence)):
        sentence[i] += '/'
        sentence[i] += tags[i]
    sentence = " ".join(sentence)
    sentence = collapse_punc(sentence)
    return sentence

def collapse_punc(sentence):
    sentence = re.sub(r'\,\s\,\/', '', sentence)
    sentence = re.sub(r'\/\.\s', '', sentence)
    return sentence

if __name__ == '__main__':
    #tweet = "Trouble in Prof. Mary, I see!!! Hmm... Mary??? Iran so far away. flockofseagullsweregeopoliticallycorrect."

    #determine whether for training data or testign data
    test_ind=False
    if ("train" in sys.argv[1]):
        group = int(sys.argv[2])    
        test_data_set = range(5500*group, 5500*(group+1)) + range(800000 + 5500*group, 5500*(group+1)+ 800000)
    elif("test" in sys.argv[1]) :
        test_ind=True
        
    abbrrev = load_list('/u/cs401/Wordlists/abbrev.english')
    pn_abbr = load_list('/u/cs401/Wordlists/pn_abbrev.english')
    m_name = load_list('/u/cs401/Wordlists/maleFirstNames.txt')
    f_name = load_list('/u/cs401/Wordlists/femaleFirstNames.txt')
    last_name = load_list('/u/cs401/Wordlists/lastNames.txt')    
    names = m_name + f_name + last_name
    abbr = abbrrev + pn_abbr      
    tagger = NLPlib.NLPlib()
 
    with open(sys.argv[1], 'rb') as csvfile:
        reader = csv.reader(csvfile)   # opens the csv file
        output_file = open(sys.argv[-1], 'wb')
        line_count = 1
        for line in reader:   # iterates the rows of the file in orders
            if test_ind or (line_count in test_data_set):
                #print(line_count)
                #The reader function will take each line of the file and make a list containing all that line's columns. 
                output_file.write('<A=' + line[0] + '>\n')
                #Only keep the tweet, discard tweet time and usrname 
                tweet = line[-1]
                tweet = remove_url(tweet)
                tweet = remove_tags(tweet)
                tweet = convert_ascii(tweet)
                tweet = remove_first_cha(tweet)
                tweet = find_end(tweet)

                for sentence in tweet:
                    sentence = tweet_tag(sentence) 
                    output_file.write(sentence)
                    output_file.write('\n')
            line_count += 1
  
    output_file.close()
 
