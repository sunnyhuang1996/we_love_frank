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

    trainfile.write("@relation train")
    valifile.write("@relation validation")

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


if __name__ == "__main__":
    main()

    
    
