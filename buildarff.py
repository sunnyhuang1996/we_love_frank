import sys


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

def count(,category):

if __name__ == '__main__':
    
    #check the validity of the input argument
    if len(sys.argv) == 3:
        num_data_each_group = sys.argv[2]
      
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
    
    #write data
    output_file.write('@data\n')
    input_file.close()
    output_file.close()
        