from numpy import array
from scipy import stats

def writetitle(output_file):
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
                      '@attribute class {0,4}\n\n' +
                      '@DATA\n')


def writelines(n):
    inputfile = open("train.arff", 'rb')

    trainfile = open("train" + str(n+1) + ".arff", 'wb')
    valifile = open("vali" + str(n+1) + ".arff", 'wb')

    trainfile.write("@relation train\n")
    valifile.write("@relation validation\n")

    writetitle(trainfile)
    writetitle(valifile)

    line_count = 1
    for line in inputfile.readlines()[25:]:
        if line_count in (range(1+550*n, 551+550*n) + range(5501+550*n, 6051+550*n)):
            valifile.write(line)
        else:
            trainfile.write(line)
        line_count+=1

    inputfile.close()
    trainfile.close()
    valifile.close()

    print "=== finish case " + str(n) + "========\n"
    print "\n"


def main():
    for i in range(0,10):
        writelines(i)


def ttest():
    SVM = array([[61.3636, 60.6, 62.23, 64.9, 57.8], [62.1818, 61.96, 62.4, 63.1, 61.3],
                 [60.3636, 59.6, 61.3, 64.4, 56.4], [58.6364, 58.6, 58.6, 58.7, 58.5],
                 [64, 63.8, 64.2, 64.5, 63.5], [61.2727, 60.2, 62.6, 66.5, 56],
                 [62.1818, 60.8, 64, 68.5, 55.8], [62, 62, 62, 62.2, 61.8],
                 [62.5455, 65.9, 63.2, 65.1, 60], [62, 61.1, 63.1, 65.6, 58.4]])


    Bayes = array([[58.3636, 60.5, 57, 48.4, 68.4], [57.9, 60.9, 56.2, 42.5, 71.6],
                   [57, 59.1, 55.7, 45.5, 68.5], [55.5, 57.4, 54.4, 42.9, 68.2],
                   [58.1, 59.7, 56.9, 49.8, 66.4], [57.72, 59.4, 56.5, 48.7, 66.7],
                   [60.4, 63.3, 58.5, 49.3, 71.5], [58.9, 61.1, 57.4, 49.1, 68.7],
                   [59.2, 61.8, 57.5, 48, 70.4], [57.5, 57.5, 56.1, 44.7, 70.4]])


    DeTree = array([[60.3, 61.5, 59.3, 54.9, 65.6], [59.4, 59.5, 59.2, 58.5, 60.2],
                    [57.9, 58.2, 57.7, 56.4, 59.5], [55.8, 55.9, 55.7, 54.7, 56.9],
                    [60.2, 60.9, 59.5, 58.4, 63.6], [58.2, 58.1, 58.3, 58.9, 57.5],
                    [58.5, 58.8, 58.1, 56.4, 60.5], [58.7, 59.1, 58.4, 56.7, 60.7],
                    [58.2, 58.2, 57.9, 56.4, 60], [59.2, 59.3, 59, 57.8, 60]])

    
    for i in range(0, 10):
        '''print "======SVM and Bayes======="
        r = stats.ttest_rel(SVM[i], Bayes[i])
        print r[1]
        
        
        #print "======SVM and Decision Tree======="
        r = stats.ttest_rel(SVM[i], DeTree[i])
        print r[1]
'''
        #print "======Bayes and Decision Tree======="
        r = stats.ttest_rel(Bayes[i], DeTree[i])
        print r[1]
        

if __name__ == "__main__":
    #main()
    ttest()
