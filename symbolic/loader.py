# Copyright: copyright.txt

import inspect
import re
import os
import sys

from symbolic.ast_rewriter.ast_rewriter import ASTRewriter
from .invocation import FunctionInvocation
from .symbolic_types import SymbolicInteger, getSymbolic

# The built-in definition of len wraps the return value in an int() constructor, destroying any symbolic types.
# By redefining len here we can preserve symbolic integer types.
import builtins
builtins.len = (lambda x : x.__len__())

# used to determine if a value is hashable, for expected output comparison. 
import collections



class Loader:
	def __init__(self, filename, entry, ast_rewrite_enabled):
		self._fileName = os.path.basename(filename)
		self._fileName = self._fileName[:-3]
		if (entry == ""):
			self._entryPoint = self._fileName
		else:
			self._entryPoint = entry;

		self.ast_rewrite_enabled = ast_rewrite_enabled

		if(self.ast_rewrite_enabled):
			print("Using PyFinder AST rewriter")
			self.ast_rewriter = ASTRewriter()
			rewritten_file = "rewritten_program.py"
			self.ast_rewriter.rewrite_file(filename, rewritten_file)  # temp dev line
			self._fileName = rewritten_file[:-3] # remove the ".py" suffix


		self._resetCallback(True)



	def getFile(self):
		return self._fileName

	def getEntry(self):
		return self._entryPoint
	
	def createInvocation(self):
		inv = FunctionInvocation(self._execute,self._resetCallback)
		func = self.app.__dict__[self._entryPoint]
		argspec = inspect.getargspec(func)
		# check to see if user specified initial values of arguments
		if "concrete_args" in func.__dict__:
			for (f,v) in func.concrete_args.items():
				if not f in argspec.args:
					print("Error in @concrete: " +  self._entryPoint + " has no argument named " + f)
					raise ImportError()
				else:
					Loader._initializeArgumentConcrete(inv,f,v)
		if "symbolic_args" in func.__dict__:
			for (f,v) in func.symbolic_args.items():
				if not f in argspec.args:
					print("Error (@symbolic): " +  self._entryPoint + " has no argument named " + f)
					raise ImportError()
				elif f in inv.getNames():
					print("Argument " + f + " defined in both @concrete and @symbolic")
					raise ImportError()
				else:
					s = getSymbolic(v)
					if (s == None):
						print("Error at argument " + f + " of entry point " + self._entryPoint + " : no corresponding symbolic type found for type " + str(type(v)))
						raise ImportError()
					Loader._initializeArgumentSymbolic(inv, f, v, s)
		for a in argspec.args:
			if not a in inv.getNames():
				# TODO: try with different seed values and data types! (currently fixed to 0)
				Loader._initializeArgumentSymbolic(inv, a, 0, SymbolicInteger)
		return inv


	# need these here (rather than inline above) to correctly capture values in lambda
	def _initializeArgumentConcrete(inv,f,val):
		inv.addArgumentConstructor(f, val, lambda n,v: val)

	def _initializeArgumentSymbolic(inv,f,val,st):
		inv.addArgumentConstructor(f, val, lambda n,v: st(n,v))

	def executionComplete(self, return_vals):
		if "expected_result" in self.app.__dict__:
			return self._check(return_vals, self.app.__dict__["expected_result"]())
		if "expected_result_set" in self.app.__dict__:
			return self._check(return_vals, self.app.__dict__["expected_result_set"](),False)
		else:
			print(self._fileName + ".py contains no expected_result function")
			return None

	# -- private

	def _resetCallback(self,firstpass=False):
		self.app = None
		if firstpass and self._fileName in sys.modules:
			print("There already is a module loaded named " + self._fileName)
			raise ImportError()
		try:
			if (not firstpass and self._fileName in sys.modules):
				del(sys.modules[self._fileName])
			self.app =__import__(self._fileName)
			if not self._entryPoint in self.app.__dict__ or not callable(self.app.__dict__[self._entryPoint]):
				print("File " +  self._fileName + ".py doesn't contain a function named " + self._entryPoint)
				raise ImportError()

			# jteoh: update 5-24, trying new process of rewriting a new file, which means we don't need to
			# do an AST rewrite each time.
			# jteoh: not sure exactly why PyExZ3 reimports each time, but
			# rewrite the function each time since we do a clean import
			#self._rewrite_AST()

		except Exception as arg:
			print("Couldn't import " + self._fileName)
			print(arg)
			raise ImportError()

	def _execute(self, **args):
		return self.app.__dict__[self._entryPoint](**args)

	def _toBag(self,l):
		bag = {}
		for i in l:
			if not isinstance(i, collections.Hashable):
				i = str(i)
			if i in bag:
				bag[i] += 1
			else:
				bag[i] = 1
		return bag

	def _check(self, computed, expected, as_bag=True):
		b_c = self._toBag(computed)
		b_e = self._toBag(expected)
		if as_bag and b_c != b_e or not as_bag and set(computed) != set(expected):
			print("-------------------> %s test failed <---------------------" % self._fileName)
			print("Expected: %s, found: %s" % (b_e, b_c))
			return False
		else:
			print("%s test passed <---" % self._fileName)
			return True

	def _rewrite_AST(self):#, func, entryPoint, namespace):
		if(self.ast_rewrite_enabled):
			self.app.__dict__[self._entryPoint] = self.ast_rewriter.rewrite(self._entryPoint, self.app.__dict__)

def loaderFactory(filename,entry, ast_rewrite_enabled):
	if not os.path.isfile(filename) or not re.search(".py$",filename):
		print("Please provide a Python file to load")
		return None
	try: 
		dir = os.path.dirname(filename)
		sys.path = [ dir ] + sys.path
		ret = Loader(filename,entry, ast_rewrite_enabled)
		return ret
	except ImportError:
		sys.path = sys.path[1:]
		return None


