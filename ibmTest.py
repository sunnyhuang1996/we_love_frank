# ibmTest.py
# 
# This file tests all 11 classifiers using the NLClassifier IBM Service
# previously created using ibmTrain.py
# 
# TODO: You must fill out all of the functions in this file following 
# 		the specifications exactly. DO NOT modify the headers of any
#		functions. Doing so will cause your program to fail the autotester.
#
#		You may use whatever libraries you like (as long as they are available
#		on CDF). You may find json, request, or pycurl helpful.
#		You may also find it helpful to reuse some of your functions from ibmTrain.py.
#

import requests
from requests.auth import HTTPBasicAuth
import json
import sys
import ast
import csv

def get_classifier_ids(username,password):
	# Retrieves a list of classifier ids from a NLClassifier service 
	# an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#		
	# Returns:
	#	a list of classifier ids as strings
	#
	# Error Handling:
	#	This function should throw an exception if the classifiers call fails for any reason
	#
	
	#TODO: Fill in this function
	
        try:
		url = 'https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers'
		result = requests.get(url, auth=(username, password))
		classifier_list = json.loads(result.text)['classifiers']

	except requests.exceptions.RequestException as error:   
		print error
		sys.exit(1)
	else:
		return_list = []
		for classifier in classifier_list:
			return_list.append(str(classifier['classifier_id']))		
		return return_list


class NotAvailableError(Exception):
	def __init__(self, classifier_id):
		self.classifier_id= classifier_id
	def __str__(self):
		return repr(self.value)
	
class CSVFormatError(Exception):
	def __init__(self, csv_file):
		self.csv_file= csv_file
	def __str__(self):
		return repr(self.value)
	
def assert_all_classifiers_are_available(username,password,classifier_id_list):
	# Asserts all classifiers in the classifier_id_list are 'Available' 
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	classifier_id_list - a list of classifier ids as strings
	#		
	# Returns:
	#	None
	#
	# Error Handling:
	#	This function should throw an exception if the classifiers call fails for any reason AND 
	#	It should throw an error if any classifier is NOT 'Available'
	#
	
	#TODO: Fill in this function
	
	for classifier in classifier_id_list:
		
		try:
		
			url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/" + classifier
			result = requests.get(url, auth=(username, password))
			#get the status for each classfier
			classifier_status = str(json.loads(result.text)['status'])
			#if classifier_status != 'Available':	
				#raise NotAvailableError(classifier)
		
		except requests.exceptions.RequestException as error:    # This is the correct syntax
			print error
			sys.exit(1)
			
		print(result.text)

		
	return

def classify_single_text(username,password,classifier_id,text):
	# Classifies a given text using a single classifier from an NLClassifier 
	# service
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	classifier_id - a classifier id, as a string
	#		
	#	text - a string of text to be classified, not UTF-8 encoded
	#		ex. "Oh, look a tweet!"
	#
	# Returns:
	#	A "classification". Aka: 
	#	a dictionary containing the top_class and the confidences of all the possible classes 
	#	Format example:
	#		{'top_class': 'class_name',
	#		 'classes': [
	#					  {'class_name': 'myclass', 'confidence': 0.999} ,
	#					  {'class_name': 'myclass2', 'confidence': 0.001}
	#					]
	#		}
	#
	# Error Handling:
	#	This function should throw an exception if the classify call fails for any reason 
	#	
	
	
	
	#TODO: Fill in this function
	
	try:
		url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/" + classifier_id + "/classify"
		result = requests.post(url, auth=(username, password), json={'text': text})
		classification = ast.literal_eval(result.text)
		print(classification)
		classification.pop('url')
		classification.pop('text')
		classification.pop('classifier_id')
		return classification
			
	except requests.exceptions.RequestException as error:  
		print error
		sys.exit(1)	

def remove_classifier(username, password, classifier_id):
	try:
	
		url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/" + classifier
		result = requests.delete(url, auth=(username, password))
		print("remove " + classifier + "-->" + str(result.status_code))
	
	except requests.exceptions.RequestException as error:    # This is the correct syntax
		print error
		sys.exit(1)
		
		
def convert_to_watson_csv_format(input_csv_name, output_csv_name): 
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
	try:
                csvfile = open(input_csv_name, 'rb')
                reader = csv.reader(csvfile)   # opens the csv file
                output_file = open(output_csv_name, 'wb')
                for line in reader:
			info = (line[-1]).strip("\n")
			info = info.strip()
			info = " ".join(info.split())
			info = info.replace('"', '') #get rid of all "
			output_file.write("\"" + info + "\"" + "," + line[0] + "\n")  #write info, class to csv
                csvfile.close()
                output_file.close()
                
        except IOError:
		print "Could not read file:", input_csv_name
		sys.exit()
		
		

def classify_all_texts(username,password,input_csv_name):
        # Classifies all texts in an input csv file using all classifiers for a given NLClassifier
        # service.
        #
        # Inputs:
        #       username - username for the NLClassifier to be used, as a string
        #
        #       password - password for the NLClassifier to be used, as a string
        #      
        #       input_csv_name - full path and name of an input csv file in the 
        #              6 column format of the input test/training files
        #
        # Returns:
        #       A dictionary of lists of "classifications".
        #       Each dictionary key is the name of a classifier.
        #       Each dictionary value is a list of "classifications" where a
        #       "classification" is in the same format as returned by
        #       classify_single_text.
        #       Each element in the main dictionary is:
        #       A list of dictionaries, one for each text, in order of lines in the
        #       input file. Each element is a dictionary containing the top_class
        #       and the confidences of all the possible classes (ie the same
        #       format as returned by classify_single_text)
        #       Format example:
        #              {'classifiername':
        #                      [
        #                              {'top_class': 'class_name',
        #                              'classes': [
        #                                        {'class_name': 'myclass', 'confidence': 0.999} ,
        #                                         {'class_name': 'myclass2', 'confidence': 0.001}
        #                                          ]
        #                              },
        #                              {'top_class': 'class_name',
        #                              ...
        #                              }
        #                      ]
        #              , 'classifiername2':
        #                      [
        #                      ...      
        #                      ]
        #              ...
        #              }
        #
        # Error Handling:
        #       This function should throw an exception if the classify call fails for any reason
        #       or if the input csv file is of an improper format.
        #

        #TODO: Fill in this function
	
	classification_dict = dict()
	classifier_list = ["c7fa49x23-nlc-998","c7e487x21-nlc-1079"]
	'''
	classifier_list = get_classifier_ids(username,password)
	for classifier in classifier_list:
		classification_dict[classifier] = list()
	'''
	with open(input_csv_name, 'rb') as csvfile:
		reader = csv.reader(csvfile)   # opens the csv file
		
		for line in reader:   # iterates the rows of the file in orders
			if len(line) != 6:
				raise CSVFormatError(input_csv_name)
			for classifier in classifier_list:
				classification_dict[classifier].append(classify_single_text(username,password,classifier,line[-1]))
			
        return classification_dict


def compute_accuracy_of_single_classifier(classifier_dict, input_csv_file_name):
	# Given a list of "classifications" for a given classifier, compute the accuracy of this
	# classifier according to the input csv file
	#
	# Inputs:
	# 	classifier_dict - A list of "classifications". Aka:
	#		A list of dictionaries, one for each text, in order of lines in the 
	#		input file. Each element is a dictionary containing the top_class
	#		and the confidences of all the possible classes (ie the same
	#		format as returned by classify_single_text) 	
	# 		Format example:
	#			[
	#				{'top_class': 'class_name',
	#			 	 'classes': [
	#						  	{'class_name': 'myclass', 'confidence': 0.999} ,
	#						  	{'class_name': 'myclass2', 'confidence': 0.001}
	#							]
	#				},
	#				{'top_class': 'class_name',
	#				...
	#				}
	#			]
	#
	#	input_csv_name - full path and name of an input csv file in the  
	#		6 column format of the input test/training files
	#
	# Returns:
	#	The accuracy of the classifier, as a fraction between [0.0-1.0] (ie percentage/100). \
	#	See the handout for more info.
	#
	# Error Handling:
	# 	This function should throw an error if there is an issue with the 
	#	inputs.
	#
	
	#TODO: fill in this function
	
	with open(input_csv_name, 'rb') as csvfile:
		reader = csv.reader(csvfile)   # opens the csv file
		line_index = 0
		correct_classfication = 0
		for line in reader:   # iterates the rows of the file in orders
			if len(line) != 6:
				raise CSVFormatError(input_csv_name)
			
			if classification_dict[line_index]['top_class'] == line[0]:
				correct_classification += 1	
	
		return (correct_classification / (line_index + 1))

def compute_average_confidence_of_single_classifier(classifier_dict, input_csv_file_name):
	# Given a list of "classifications" for a given classifier, compute the average 
	# confidence of this classifier wrt the selected class, according to the input
	# csv file. 
	#
	# Inputs:
	# 	classifier_dict - A list of "classifications". Aka:
	#		A list of dictionaries, one for each text, in order of lines in the 
	#		input file. Each element is a dictionary containing the top_class
	#		and the confidences of all the possible classes (ie the same
	#		format as returned by classify_single_text) 	
	# 		Format example:
	#			[
	#				{'top_class': 'class_name',
	#			 	 'classes': [
	#						  	{'class_name': 'myclass', 'confidence': 0.999} ,
	#						  	{'class_name': 'myclass2', 'confidence': 0.001}
	#							]
	#				},
	#				{'top_class': 'class_name',
	#				...
	#				}
	#			]
	#
	#	input_csv_name - full path and name of an input csv file in the  
	#		6 column format of the input test/training files
	#
	# Returns:
	#	A tuple of average confidence of the classifier, as a number between [0.0-1.0]
	#	See the handout for more info.
	#
	# Error Handling:
	# 	This function should throw an error if there is an issue with the 
	#	inputs.
	#
	
	#TODO: fill in this function
	
	with open(input_csv_name, 'rb') as csvfile:
		reader = csv.reader(csvfile)   # opens the csv file
		line_index = 0
		neg_confidence = 0
		neg_count = 0
		pos_confidence = 0
		pos_count = 0

		for line in reader:   # iterates the rows of the file in orders
			if len(line) != 6:
				raise CSVFormatError(input_csv_name)
			
			if (line[0] == '4') and (classification_dict[line_index]['top_class'] == line[0]):
				pos_count += 1
				for class_info in classification_dict[line_index]['classes']:
					if class_info['class_name'] == '4':
						pos_confidence += class_info['confidence']
	
			if (line[0] == '0') and (classification_dict[line_index]['top_class'] == line[0]):
				neg_count += 1
				for class_info in classification_dict[line_index]['classes']:
					if class_info['class_name'] == '0':
						neg_confidence += class_info['confidence']			
	
		return (pos_confidence / pos_count, neg_confidence / neg_count)



if __name__ == "__main__":

	input_test_data = ''
	username='5946518f-f870-4f75-be57-baa2ca0f4f89'
	password='MZ8VMedaeStu'
	
	#STEP 1: Ensure all 3 classifiers are ready for testing
	classifier_id_list = get_classifier_ids(username, password)
	'''
	classify_single_text(username,password,'c7fa49x23-nlc-998', 'i lam so in love with Bobby Flay... he is my favorite. RT @terrysimpson: @bflay you need a place in Phoenix. We have great peppers here!')
	'''
	#STEP 2: Test the test data on all classifiers
	assert_all_classifiers_are_available(username, password, classifier_id_list)
	#STEP 3: Compute the accuracy for each classifier
	#STEP 4: Compute the confidence of each class for each classifier

	'''
	testing_csv = '/u/cs401/A1/tweets/testdata.manualSUBSET.2009.06.14.csv'
	classifier_dict = classify_all_texts(username,password,testing_csv)
	accuracy = compute_accuracy_of_single_classifier(classifier_dict, testing_csv)
	print(accuracy)
	'''
	testing_csv = '/u/cs401/A1/tweets/testdata.manualSUBSET.2009.06.14.csv'
	classifier_dict = classify_all_texts(username,password,testing_csv)	
	
	'''
	for classifier in classifier_id_list:
		remove_classifier(username, password, classifier)
	
	'''