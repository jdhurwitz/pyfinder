# Python Basic Calculator

## Credits
	M. Bonet and Greg Hewgill (https://github.com/ghewgill/text2num)

## Definition

	Calculator which supports the basic operations on integers. 
	It works with English words for numbers and operators.

	The calculator input is read from stdin consisting of one expression 
	per line and terminated by an empty line. The results are written to 
	stdout, one result per line. See sample input and output.

	In case of errors it should emit "ERROR" as the calculation result. 
	If any intermediate result is outside the range of valid numbers this 
	is also considered an error.

	Valid Operators:
		+, plus
		-, minus
		*, times
		/, divided by

	Numbers all integers in the range -9.999.999 to 9.999.999 (inclusive) 
	the English words for all integers in the above range, e.g. "minus two thousand and one"

	Sample Input            Sample output
	--------------          ---------------
	7 + 2                   9
	8/3                     2
	3 divided by 0          ERROR
	twenty one times 2      42
	<empty line>

## How to run
	
	Run application:
	dev@localhost:~/home/calc$ ./calc.py
	or
	dev@localhost:~/home/calc$ python calc.py

	Run tests:
	dev@localhost:~/home/calc$ nosetests tests.py
	
