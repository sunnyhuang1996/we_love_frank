# ibmTrain.py
# 
# This file produces 3 classifiers using the NLClassifier IBM Service
# 
# TODO: You must fill out all of the functions in this file following 
# 		the specifications exactly. DO NOT modify the headers of any
#		functions. Doing so will cause your program to fail the autotester.
#
#		You may use whatever libraries you like (as long as they are available
#		on CDF). You may find json, request, or pycurl helpful.
#

###IMPORTS###################################
#TODO: add necessary imports
import csv  
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()
import json
import sys


###HELPER FUNCTIONS##########################

def convert_training_csv_to_watson_csv_format(input_csv_name, group_id, output_csv_name): 
	# Converts an existing training csv file. The output file should
	# contain only the 11,000 lines of your group's specific training set.
	#
	# Inputs:
	#	input_csv - a string containing the name of the original csv file
	#		ex. "my_file.csv"
	#
	#	output_csv - a string containing the name of the output csv file
	#		ex. "my_output_file.csv"
	#
	# Returns:
	#	None
	
	#TODO: Fill in this function
	test_data_set = range(5500*group_id, 5500*(group_id+1)) + range(800000 + 5500*group_id, 5500*(group_id+1)+ 800000)

	try:
                csvfile = open(input_csv_name, 'rb')
                reader = csv.reader(csvfile)   # opens the csv file
                output_file = open(output_csv_name, 'wb')
                line_count=1
                for line in reader:
                        if line_count in test_data_set:
				print line
				info = (line[-1]).strip("\n")
				info = info.strip()
				info = " ".join(info.split())
				info = info.replace('"', '') #get rid of all "
				output_file.write(info + "," + line[0] + "\n")  #write info, class to csv
                        line_count += 1
                csvfile.close()
                output_file.close()
                
        except IOError:
		print "Could not read file:", input_csv_name
		sys.exit()
		
        

               

	
def extract_subset_from_csv_file(input_csv_file, n_lines_to_extract, output_file_prefix='ibmTrain'):
	# Extracts n_lines_to_extract lines from a given csv file and writes them to 
	# an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
	#
	# Inputs: 
	#	input_csv - a string containing the name of the original csv file from which
	#		a subset of lines will be extracted
	#		ex. "my_file.csv"
	#	
	#	n_lines_to_extract - the number of lines to extract from the csv_file, as an integer
	#		ex. 500
	#
	#	output_file_prefix - a prefix for the output csv file. If unspecified, output files 
	#		are named 'ibmTrain#.csv', where # is the input parameter n_lines_to_extract.
	#		The csv must be in the "watson" 2-column format.
	#		
	# Returns:
	#	None
	
	#TODO: Fill in this function

	try:
                csvfile = open(input_csv_file, 'rb')

                output_file = open(output_file_prefix+str(n_lines_to_extract)+'.csv', 'wb')
                line_count = 1
                test_data_set = range(1, n_lines_to_extract+1) + range(5500, 5501 + n_lines_to_extract)
                
                for line in csvfile.readlines():   
                        if line_count in test_data_set:
                                output_file.write(" ".join(line.split()) + "\n")  #write info, class to csv
                                line_count += 1
                        else:
                                continue
                csvfile.close()
                output_file.close()
                
        except IOError:
		print ("Could not read file:", input_csv_file)
		sys.exit()
		
        


	
	
def create_classifier(username, password, n, input_file_prefix='ibmTrain'):
	# Creates a classifier using the NLClassifier service specified with username and password.
	# Training_data for the classifier provided using an existing csv file named
	# ibmTrain#.csv, where # is the input parameter n.
	#
	# Inputs:
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	n - identification number for the input_file, as an integer
	#		ex. 500
	#
	#	input_file_prefix - a prefix for the input csv file, as a string.
	#		If unspecified data will be collected from an existing csv file 
	#		named 'ibmTrain#.csv', where # is the input parameter n.
	#		The csv must be in the "watson" 2-column format.
	#
	# Returns:
	# 	A dictionary containing the response code of the classifier call, will all the fields 
	#	specified at
	#	http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/natural-language-classifier/api/v1/?curl#create_classifier
	#   
	#
	# Error Handling:
	#	This function should throw an exception if the create classifier call fails for any reason
	#	or if the input csv file does not exist or cannot be read.
	#
	
	url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers"

	csv_file = input_file_prefix+str(n)+'.csv'
	params = {'language': 'en', 'name': 'Classifier ' + str(n)}
	try:
		training_file = open(csv_file, 'rb')
		response = requests.post(url, auth=(username, password), \
		                         files=[('training_metadata', ('training.json', json.dumps(params))),('training_data', training_file)])
		training_file.close()
	except IOError:
		print ("Could not read file:", csv_file)
		sys.exit()
	
	try:
		return json.loads(response.text)
	except:
		raise Exception("Error processing the request, HTTP: %d" % response.status_code)		

	
if __name__ == "__main__":
	
	subset = [500, 2500, 5000]
	### STEP 1: Convert csv file into two-field watson format
        '''
	input_csv_name = '/u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv'
	#DO NOT CHANGE THE NAME OF THIS FILE
	output_csv_name ='training_11000_watson_style.csv'	
	convert_training_csv_to_watson_csv_format(input_csv_name, 2, output_csv_name);
	
	
	### STEP 2: Save 3 subsets in the new format into ibmTrain#.csv files
	
	#TODO: extract all 3 subsets and write the 11 new ibmTrain#.csv files
	#
	# you should make use of the following function call:
	#
	
	for n_lines_to_extract in subset:
                extract_subset_from_csv_file(output_csv_name,n_lines_to_extract)
	'''
	### STEP 3: Create the classifiers using Watson
	
	#TODO: Create all 11 classifiers using the csv files of the subsets produced in 
	# STEP 2
	# 
	#
	# you should make use of the following function call

	username = '5946518f-f870-4f75-be57-baa2ca0f4f89'
	password = 'MZ8VMedaeStu'

	for n in subset:
                create_classifier(username, password, n, input_file_prefix='ibmTrain')

