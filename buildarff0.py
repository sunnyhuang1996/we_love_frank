import sys
import re

only_alph = re.compile('[\W_]+') #leave only alphabet char
tag = re.compile(r'/[a-zA-Z]+') #determine tags

#===================category dict=======================
ca_dict = {
'FPP': ["I", "me", "my", "mine", "we", "us", "our", "ours"], #first person pronouns
'SPP': ["you", "your", "yours", "u", "ur", "urs"], #second person pronouns
'TPP': ["he", "him", "his", "she", "her", "hers", "it", "its", "they", "them", "their", "theirs"], #third person pronouns
'CC': ["CC"], #Coordinating conjunctions
'PTV': ["VBD", "VBN"], # Past-tense verbs
'FTV': ["'ll", "will", "gonna"], #, "going to VB"] #future tense
'CO': [","], # Commas
'CSC': [":", ";"], #Colons and semi-colons
'DASH': ["-"], #Dashes
'PA': ["("], #Parentheses
'EL': ["./:"], #Ellipses
'CN': ["NN", "NNS"], # Common Nouns
'PN': ["NNP", "NNPS"], #Proper Nouns
'ADV': ["RB", "RBR", "RBS"], #adverbs
'WW': ["WDT", "WP", "WP$", "WRB"], # wh-words
'MSA': ["smh", "fwb", "lmfao", "lmao", "lms", "tbh", "rofl", "wtf", "bff", "wyd", "lylc", "brb", "atm", "imao", "sml", "btw",
"bw", "imho", "fyi", "ppl", "sob", "ttyl", "imo", "ltr", "thx", "kk", "omg", "ttys", "afn", "bbs", "cya", "ez", "f2f", "gtr",
"ic", "jk", "k", "ly", "ya", "nm", "np", "plz", "ru", "so", "tc", "tmi", "ym", "ur", "u", "sol"] # modern slang acronyms
}

ca_list = ["FPP", "SPP", 'TPP', 'CC', 'PTV', 'FTV', 'CO', 'CSC', 'DASH', 'PA', 'EL',
           'CN', 'PN', 'ADV', 'WW', 'MSA', 'upper'];
#===================================================

"""
First/second/third person pronouns  --> /u/cs401/Wordlists/*-person
Coordinating conjunctions (CC): and, but, for, nor, or, so, and, yet	
Pat and future tense verbs come up with general rules and watch out for irregular verb

Perfective aspect (has/ have eaten) should be counted as one token

# of common nouns (NN, NNs)
# of proper nouns (NNP, NNPs)
# of adverbs (RB, RBR, RBS)
# of wh-words (WDT, WP, WP$, WRB)

"""

def aggre_count(s, categories="all"):
    '''return list of count of apperence of words in categories in string s'''
    
    L = []
    # count all category
    if categories != "all":
        for c in categories:
            L.append(assign_cate(s, c))
    #count for partial categories
    else:
        for c in ca_list:
            L.append(assign_cate(s, c))
            
    return L
    

def assign_cate(s, category):
    '''determine which category of words is calling'''
    
    # words category
    if category in ["FPP", "SPP", "TPP", "CSC", "DASH"]:
        return count(s,category, post="/")
    elif category=="EL":
        return count(s, category)
    elif category=="MSA":
        return sum([(s.upper()).count(word.upper()+"/") for word in ca_dict["MSA"]])
    # tag category
    elif category in ["CC", "CO", "PA", "CN", "PN", "ADV", "WW", "PTV"]:
        return count(s,category, pre="/", post=" ")
    #if future tense
    elif category=="FTV":
        return (len(re.findall('going/VBG to/TO [a-zA-Z]+/VB', s)) + count(s,"FTV", post="/"))
    elif category=="upper":
        sp = s.split(" ")
        return sum([(c.isupper() and c.index("/")>2) for c in sp])

    
def count(s, category, pre='', post=''):
    '''count number of appereance of word in string s'''

    return sum([s.count(pre+word+post) for word in ca_dict[category]])


def main():
        
    #check the validity of the input argument
    #if train with partial training data
    if len(sys.argv) == 4:
        num_data_each_group = sys.argv[3]
        classrange = range(0, int(num_data_each_group)+1) + range(5500, 5500+int(num_data_each_group))
    else: # all training data
        classrange = range(0, 11000)
    
    input_file = open(sys.argv[1], 'rb') #open the tweet file
    output_file = open(sys.argv[2], 'wb') 
    
    # write the relation name
    output_file.write('@relation ' + sys.argv[1][:-5] + '\n\n')
    
    #write the attribute names
    output_file.write('@attribute first_person_pronoun numeric\n' +
                      '@attribute second_person_pronoun numeric\n' +
                      '@attribute third_person_pronoun numeric\n' +
                      '@attribute coordinating_conj numeric\n' +
                      '@attribute past_tense_verb numeric\n' +
                      '@attribute future_tense_verb numeric\n' +
                      '@attribute commas numeric\n' +
                      '@attribute colons_semi_colon numeric\n' +
                      '@attribute dash numeric\n' +
                      '@attribute parentheses numeric\n' +
                      '@attribute ellipses numeric\n' +
                      '@attribute common_noun numeric\n' +
                      '@attribute proper_noun numeric\n' +
                      '@attribute adverb numeric\n' +
                      '@attribute wh_word numeric\n' +
                      '@attribute modern_slan_acronym numeric\n' +
                      '@attribute word_all_in_upper_case numeric\n' +
                      '@attribute average_length_sentence numeric\n' +
                      '@attribute average_length_token numeric\n' +
                      '@attribute number_of_sentence numeric\n' +
                      '@attribute class {0,4}\n\n'+
                      '@DATA\n')

    #=============count features ===============
    
    num_token = 0  #general token
    char_token = 0  #token of only character
    num_sen = 0  #number of sentence in tweeter
    num_char = 0  #number of cahracter in tweeter
    tweet_count=-1 #position of current tweeter
    first_line=True  #indicator of first line

    for line in input_file.readlines():   # iterates the rows of the file in orders
        #first line of tweeter
        if line.strip()=="<A=0>" or line.strip()=="<A=4>":
            tweet_count+=1  # the tweet_count th tweet
            if (tweet_count in classrange) and (not first_line):
                try:  #in case tweet doesn't have sentence & tokens 
                    avg_len_sentence = float(num_token)/num_sen  #Average length of sentences (in tokens)
                    avg_len_token = float(num_char)/char_token   #Average length of tokens, excluding punctuation tokens (in characters)
                except ZeroDivisionError:
                    avg_len_sentence=0
                    avg_len_token=0
                 
                cal+=[avg_len_sentence, avg_len_token, num_sen]  #result
                output_file.write((str(cal)[1:-1]).replace(" ","") + ", "+ line[3] + "\n") #write result to ouput file
                #----re-initialize----
                num_token = 0 
                char_token = 0 
                num_sen = 0
                num_char = 0
                class_ind=line[3]  #class indicator
                
            elif first_line:
                first_line=False
                class_ind=line[3]
                
            else:
                continue
            
        #content of tweeter
        elif tweet_count in classrange:
            num_sen +=1
            cal = aggre_count(line)  #calculate fieatures of tweeter
            past_num = len(re.findall('((have)|(has)|(had))/[a-zA-Z ]+e(n|d)/', line)) #number of past time verb
            #number of futurn time verb
            futurn_num = len(re.findall('going/VBG to/TO [a-zA-Z]+/VB', line))*2 + line.count("will") + line.count("'ll") + line.count("gonna")
            num_token += len(line.split(" ")) - past_num - futurn_num  #number of tokens (all kinds)
            line = tag.sub('', line)
            char_token += len((only_alph.sub(' ', line)).split()) - past_num - futurn_num  #number of tokens (only char)
            num_char += len(only_alph.sub('', line))  #number only char in tweeter

    if len(sys.argv) == 3: #if all data, write result for last tweeter, otherwise skip       
        avg_len_sentence = float(num_token)/num_sen
        avg_len_token = float(num_char)/char_token
        cal+=[avg_len_sentence, avg_len_token, num_sen]  #result
        output_file.write((str(cal)[1:-1]).replace(" ","") + ", 4\n")
    #============================
        
    #write data   
    input_file.close()
    output_file.close()


if __name__ == '__main__':
    main()
