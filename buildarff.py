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
    if categories != "all":
        for c in categories:
            L.append(assign_cate(s, c))
    else:
        for c in ca_list:
            L.append(assign_cate(s, c))
            
    return L
    

def assign_cate(s, category):
    '''determine which category of words is calling'''
    #if words
    if category in ["FPP", "SPP", "TPP", "CSC", "DASH", "EL", "MSA"]:
        return count_word(s,category)
    #if tag
    elif category in ["CC", "CO", "PA", "CN", "PN", "ADV", "WW", "PTV"]:
        return count_type(s,category)
    #if future tense
    elif category=="FTV":
        return (len(re.findall('going/VBG to/TO [a-zA-Z]+/VB', s)) + count_word(s,"FTV"))
    elif category=="upper":
        sp = s.split(" ")
        return sum([(c.isupper() and c.index("/")>2) for c in sp])
    

def count_word(s,category):
    '''
    count the total number of apperence of words in category in string s
    '''
    if category=="EL":
        return sum([s.count(word) for word in ca_dict[category]])
    elif category=="MSA":
        return sum([s.count(word+"/") for word in ca_dict[category]]) + sum([s.count(word.upper()+"/") for word in ca_dict[category]])
    else:
        return sum([s.count(word+"/") for word in ca_dict[category]])
        

def count_type(s, category):
    '''
    count the total number of apperence tags in category in string s
    '''
    return sum([s.count("/"+tag+" ") for tag in ca_dict[category]])

 

if __name__ == '__main__':
    #check the validity of the input argument
    if len(sys.argv) == 4:
        num_data_each_group = sys.argv[3]
    classrange = range(0, int(num_data_each_group)) + range(5500, 5500+int(num_data_each_group))
    
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
                      '@attribute class numeric\n\n')
    

    #input_file = open('sample.twt', 'rb')
    #================
    #Average length of sentences (in tokens)
    #Average length of tokens, excluding punctuation tokens (in characters)
    #Number of sentences
    
    
    num_token = 0 #general token
    char_token = 0 #token of only character
    num_sen = 0
    num_char = 0
    tweet_count=1

    for line in input_file.readlines()[1:]:   # iterates the rows of the file in orders
        if line.strip()=="<A=0>" or line.strip()=="<A=4>":
            tweet_count+=1
            if tweet_count in classrange:
                print str(tweet_count) + "------"
                try:
                    avg_len_sentence = float(num_token)/num_sen
                    avg_len_token = float(num_char)/char_token
                except ZeroDivisionError:
                    avg_len_sentence=0
                    avg_len_token=0
                 
                cal+=[avg_len_sentence, avg_len_token, num_sen]  #result
                print cal
                output_file.write(str(cal)+"\n")
                num_token = 0 #general token
                char_token = 0 #token of only character
                num_sen = 0
                num_char = 0
                
            else:
                continue
            
         
        elif tweet_count in classrange:
            num_sen +=1
            cal = aggre_count(line)
            past_num = len(re.findall('((have)|(has)|(had))/[a-zA-Z ]+e(n|d)/', line)) #past time verb
            #futurn time verb
            futurn_num = len(re.findall('going/VBG to/TO [a-zA-Z]+/VB', line))*2 + line.count("will") + line.count("'ll") + line.count("gonna")
            num_token += len(line.split(" ")) - past_num - futurn_num #number of tokens (all kinds)
            line = tag.sub('', line)
            char_token += len((only_alph.sub(' ', line)).split()) - past_num - futurn_num
            num_char += len(only_alph.sub('', line))

            
    avg_len_sentence = float(num_token)/num_sen
    avg_len_token = float(num_char)/char_token
    cal+=[avg_len_sentence, avg_len_token, num_sen]  #result
    output_file.write(str(cal)+"\n")
    print cal
    #=================
                  
    
    #write data
    
    input_file.close()
    output_file.close()
    #nrc saif NLP NRC Emotion Lexicon

