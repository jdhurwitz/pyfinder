#!/usr/bin/python
#
# Copyright 2012 M.Bonet.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from symbolic.args import *
"""
	Write a calculator which supports the basic operations on integers. 
	The calculator should also work with English words for numbers and operators.

	The calculator input is read from stdin consisting of one expression 
	per line and terminated by an empty line. The results are written to 
	stdout, one result per line. See sample input and output.

	The program should always terminate with an exit status of zero. 
	In case of errors it should emit "ERROR" as the calculation result. 
	If any intermediate result is outside the range of valid numbers this 
	is also considered an error.

	Valid Operators:
		+, plus
		-, minus
		*, times
		/, divided by

	There can be up to 10 operators in a single expression.
	Numbers all integers in the range -9.999.999 to 9.999.999 (inclusive) 
	the English words for all integers in the above range, e.g. "minus two thousand and one"

	Sample Input		Sample output
	--------------		---------------
	7 + 2			9
	8/3			2
	3 divided by 0	 	ERROR
	twenty one times 2	42
	<empty line>

"""

__author__ = "M.Bonet"
__copyright__ = "Copyright 2012, M.Bonet"
__credits__ = ["M.Bonet", "Greg Hewgill"]
__license__ = "GPL"
__version__ = "0.0.1"


import operator
import text2num

operator_alias = {
	'+': ['plus','mas'],
	'-': ['minus', 'menos'],
	'*': ['multiply by','times', 'time', 'por', 'vez', 'veces'],
	'/': ['dividido por', 'divided by', 'dividido', 'div']
}

operator_mask = {
	'+': operator.add,
	'-': operator.sub,
	'*': operator.mul,
	'/': operator.truediv
}

def calc_expr(operation, item1=0, item2=0):
	'''
		Given a operation first term and second term we proceed 
		to perform the operation and return the result.

		Argument:
		operation -- operation we want to perform ["*","/","+","-"]
		item1 -- first term of the operation
		item2 -- second term of the operation

		Example:
			@input: string="+", item1="4", item2="5" 
			@output: 9
	'''
	op = operator_mask[operation](int(item1), int(item2))
	return op

def is_operator(character):
	return character in operator_alias

def previous_operator(string):
	reversed_string = string[::-1]
	return next_operator(reversed_string)

def next_operator(string):
	for c in string:
		if is_operator(c):
			return c
	return False

def is_minus_sign(string):
	return string.count('-') == 1 and string.index('-') == 0

def still_operators(string):
	for operation in operator_alias:
		if string.count(operation) > 0 and not (operation == '-' and is_minus_sign(string)): 
			return True
	return False

def get_terms(string, position):
	'''
		Given a mathematical string and a position which matches with an operation
		extracts the two terms are involved.

		Argument:
		string -- inline mathematical operations
		position -- position where operator is

		Example:
			@input: string="1+3-4", position="4" 
			@output: ("3","4")
	'''

	#-- Split the string in two parts by the operator --
	string_item1 = string[:position]
	string_item2 = string[position+1:]

	#-- Looking for size of the first term --
	previous_operation = previous_operator(string_item1)
	if previous_operation:
		item1 = string_item1.split(previous_operation)[-1]

		#-- If previous operator is "-" we assume is the sign of the number and we add it --
		if previous_operation == '-' and is_minus_sign(string_item1):
			item1 = '-' + item1
	else:
		item1 = string_item1

	#-- Looking for size of the second term --
	next_operation = next_operator(string_item2)
	if next_operation:
		item2 = string_item2[0:string_item2.index(next_operation)]
	else:
		item2 = string_item2

	return (item1, item2, next_operation)

def run(string):
	'''
		Given a mathematical string tries to calculate all the operations inside

		Argument:
		string -- inline mathematical operations 

		Example:
			@input: "1+3-4"
			@output: "0"
	'''
	
	#-- Until we don't find more operators in the string we keep looping --
	# jteoh: added to prevent premature return, but in practice we should have a check here?
	result = string
	while still_operators(string):

		operation = next_operator(string)
		position = string.index(operation)
		
		#-- Avoiding (-) symbol at the beginning --
		if operation == '-' and position == 0: 
			substring = string[1:]
			operation = next_operator(substring)

			if not operation:
				break
			
			subposition = substring.index(operation)
			position += subposition + 1 

		#-- Getting terms involve in the operation --
		(item1, item2, next_operation) = get_terms(string, position)
		string = string[position+len(item2)+1:]

		#-- If current operation is + or - and next operation is / or *
		#-- the second one has preference over the first one. Otherwise we just calc_exprulate --
		if next_operation and operation in ['+','-'] and next_operation in ['/','*']:
			(_, item3, _) = get_terms(string,0)
			item2 = calc_expr(next_operation, item2, item3)
			string = str(item1) + operation + str(item2) + string[len(item3)+1:]
		else:
			result = calc_expr(operation, item1, item2)
			string = str(result) + string

	return result

"""
JH: commented out because this is no longer being used for the simplified case.
def normalize_operators(line):
	'''
		Gets a simple string and tries to match with certain aliases
		if operators has been passed as English/Spanish word

		Argument:
		line -- string we want to normalize

		Example:
			@input: "1 plus 3 minus 4"
			@output: "1 + 3 - 4"
	'''

	for symbol, posible_alias in operator_alias.iteritems():
		for alias in posible_alias:
			line = line.replace(alias, symbol)

	return line
	
"""

"""
JH: commented out because this is no longer being used for the simplified case.
def normalize_numbers(line):
	'''
		Gets a simple string and tries to match with certain aliases
		if numbers has been passed as English word

		Argument:
		line -- string we want to normalize

		Example:
			@input: "one + three - four"
			@output: "1 + 3 - 4"
	'''

	result = ""

	#-- If line starts with (-) or (+) we keep this for the result --
	if line[0] in ['+','-']:
		result = line[0]
		line = line[1:]

	subline = line
	list_operations = []	
	while next_operator(subline):
		operation = next_operator(subline)
		position = subline.index(operation)
		subline = subline[position+1:]
		list_operations.append(operation)

	subline = line
	for operation in operator_alias:
		subline = subline.replace(operation, '#')
	list_words = subline.split('#')
	
	for position in range(len(list_words)):
		word = list_words[position].strip()
		try: 
			int(word)
		except ValueError:
			word = str(text2num.text2num(word))
		
		result += word 
		if position < len(list_operations):
			result += list_operations[position]

	return result
"""

"""
JH: this function was used to pull input from CLI - no longer needed because symbolic seed is entered by us.
def get_input(title):
	'''
		Builds a list based on input from console. All input will be wrap in a list of 
		lines thanks to a endless loop until user leaves empty line.

		Argument:
		title -- Phrase will be shown in the console waiting for user input. 

		Example:
			@input:
			>>>
			1+3-4
			22+34			
			<empty_line>

			@output:["1+3-4","22+34"]
			
	'''

	result = []
	item = input(title)
	result.append(item)
	
	while True:
		item = input()
		if not item: break
		result.append(item)

	return result

"""

def check_chars(line):
	new_str = ""
	acceptable_chars  = ['+', '-', '/', '*', '0','1','2','3','4', '5','6','7', '8', '9']

	# for i in range(len(line)): # calls __len__ and __getitem__
	# 	if line[i] not in acceptable_chars:
	for char in line: # calls __iter__
		if char not in acceptable_chars:
			return False

	return True

@symbolic(a="2+5-1")
def calc(a):
	#line = normalize_operators(a)
	#line = normalize_numbers(line)


	#TODO: add this back in -> removed for testing simplification
	#line = a.replace(' ','')
	line = a
	if len(line) == 0:
		return("Error: empty string")

	#NOTE: this works as expected -> pyexz3 will test inputs that break this
	if not check_chars(line):
		return("Error: not all nums or operator")

	# -- Validate --
	# -- First value can only by (-) minus symbol or (+) plus symbol --
	if line[0] in ['*', '/']:
		return("Error 001 - Operator(* or /) can't be at the beginning of the instruction")


	# -- Last value can not be any kind of operator --
	if line[-1] in operator_alias:
		return("Error 002 - Operator (* or /) can't be at the end of the instruction")

	return(str(run(line)))

"""
if __name__=="__main__":

	input_result = get_input("Please type your calculation request:\n")
	while True:
		try:
			print("Result:")

			for line in input_result:
				try:
					#-- Normalize alias for operator --
					#line = normalize_operators(line)
				

					#-- Convert all possible number-words to numer --
		#			line = normalize_numbers(line)

					#-- Removing empty spaces --
					line = line.replace(' ','')

					#-- Validate --
					#-- First value can only by (-) minus symbol or (+) plus symbol --
					if line[0] in ['*','/']:
						print("Error 001 - Operator(* or /) can't be at the beginning of the instruction")
						continue

					#-- Last value can not be any kind of operator --
					if line[-1] in operator_alias:
						print("Error 002 - Operator (* or /) can't be at the end of the instruction")
						continue
				
					#-- Printing result --
					res = str(run(line))
					print(res)

				except ZeroDivisionError:
					print("ERROR")
				except text2num.NumberException:
					print("ERROR - Word number")
				except:
					print("Unhandled error, please contact me. Hint: check your input string.")
				

			#-- Asking for next or just exiting --
			input_result = get_input("\nPlease type another request or Control+C to exit:\n")

		except KeyboardInterrupt:
			print("Bye!")
			break

"""