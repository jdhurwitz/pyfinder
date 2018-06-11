# Copyright: see copyright.txt

import os
import sys
import logging
import traceback
from optparse import OptionParser

from symbolic.loader import *
from symbolic.explore import ExplorationEngine
from symbolic.test_suite_generator import test_suite_generator
from inspect import getmembers, isfunction
import importlib

sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__)))] + sys.path

usage = "usage: %prog [options] <path to a *.py file>"
parser = OptionParser(usage=usage)

parser.add_option("-l", "--log", dest="logfile", action="store", help="Save log output to a file", default="")
parser.add_option("-s", "--start", dest="entry", action="store", help="Specify entry point", default="")
parser.add_option("-g", "--graph", dest="dot_graph", action="store_true", help="Generate a DOT graph of execution tree")
parser.add_option("-m", "--max-iters", dest="max_iters", type="int", help="Run specified number of iterations", default=0)
parser.add_option("--cvc", dest="cvc", action="store_true", help="Use the CVC SMT solver instead of Z3", default=False)
parser.add_option("--z3", dest="cvc", action="store_false", help="Use the Z3 SMT solver")
parser.add_option("--rewrite_ast", dest="ast_rewrite_enabled", action="store_true", default=False,
				  help="Disable AST rewriting of application program")
parser.add_option("--debug_ast", dest="debug_ast", action="store_true", default=False, help="Print AST during rewrite")
parser.add_option("--generate_test_suite", dest="test_suite_enabled", action="store_true", default=False, help="Generage a python test suite file")
parser.add_option("--evaluate_all_funcs", dest="evaluate_all_funcs", action="store_true", default=False, help="Run on all functions in specified file")
parser.add_option("--try-multiple-seeds", dest="try_multiple_seeds", action="store_true", default=False, help="Attempt multiple symbolic seed values (eg 0, -1, 1, '', 'foo') if exceptions occur")
(options, args) = parser.parse_args()

if options.entry and options.evaluate_all_funcs:
	print("Do not specify entry function if running over all functions")
	sys.exit(0)

if not (options.logfile == ""):
	logging.basicConfig(filename=options.logfile,level=logging.DEBUG)

if len(args) == 0 or not os.path.exists(args[0]):
	parser.error("Missing app to execute")
	sys.exit(1)

solver = "cvc" if options.cvc else "z3"

print("PyExZ3 (Python Exploration with %s)" % solver.upper())

filename = os.path.abspath(args[0])

allEntries = []
allGeneratedInputs = []
allReturnVals = []

def run():
	# Get the object describing the application
	app = loaderFactory(filename,options.entry, options.ast_rewrite_enabled, options.debug_ast)
	if app == None:
		sys.exit(1)

	print ("Exploring " + app.getFile() + "." + app.getEntry())

	result = None
	try:
		generatedInputs, path, returnVals = create_and_run_invocations(app, options.try_multiple_seeds)

		allEntries.append(app.getEntry())
		allGeneratedInputs.append(generatedInputs)
		allReturnVals.append(returnVals)

		# check the result
		result = app.executionComplete(returnVals)

		# output DOT graph
		if (options.dot_graph):
			file = open(filename+".dot","w")
			file.write(path.toDot())	
			file.close()

	except ImportError as e:
		# createInvocation can raise this
		logging.error(e)
		sys.exit(1)

	return result


def create_and_run_invocations(app, try_multiple_seeds=False):
	""" Terrible way of handling multiple seed values.
	Function Invocation internally keeps track of how many possible combinations there are.
	We recreate the engine and execute for each possible combination, if that combination yields an error.
	Ideally we'd do this within the exploration engine itself - here, we'll retry even if some inputs are properly
	generated (ie an error appears perhaps in the 5th execution)

	tl;dr: This will retry until all seed values are exhausted or any input results in a complete error-free exploration
	(not just one execution)

	Alternatively: we'd somehow retain the generated inputs and save them for test cases...
	"""
	invocation = app.createInvocation()
	try:
		return run_invocation(invocation)
	except ImportError as e:
		# rethrow import errors, as no symbolic arguments will help here and that is the original behavior.
		raise
	except Exception as init_error:
		if try_multiple_seeds:
			print("Input yielded error: " + str(init_error))
			for _ in range(invocation.num_seed_assignments):
				print()
				print("Trying new set of initial seed arguments")
				try:
					vals = run_invocation(invocation)
					return vals
				except Exception as e:
					print("Input yielded error: " + str(e))
					# raise e
					pass
			raise Exception("No default argument assignments resulted in error-free execution!")
		else:
			raise



def run_invocation(invocation):
	engine = ExplorationEngine(invocation, solver=solver)
	generatedInputs, returnVals, path = engine.explore(options.max_iters)
	return generatedInputs, path, returnVals


if options.evaluate_all_funcs:
	directory = os.path.dirname(filename)
	sys.path.append(directory)
	module_name = os.path.basename(filename)[:-3]
	module = importlib.import_module(module_name)
	functions_list = [o[0] for o in getmembers(module) if isfunction(o[1])]	
	for function in functions_list:
		del sys.modules[module_name]
		if function != "expected_result":
			options.entry = function
			result = run()

else:
	result = run()

#output test suite
if (options.test_suite_enabled):
	test_suite_generator(filename, allEntries, allGeneratedInputs, allReturnVals)

if result == None or result == True:
	sys.exit(0)
else:
	sys.exit(1);	

