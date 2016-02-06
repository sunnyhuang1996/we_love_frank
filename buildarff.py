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

if __name__ == '__main__':
    
    #check the validity of the input argument
    if len(sys.argv) == 3:
        num_data_each_group = sys.argv[2]
      
    input_file = open(sys.argv[1], 'rb') #open the tweet file 
    output_file = open(sys.argv[2], 'wb')   
    
    input_file.close()
    output_file.close()
        