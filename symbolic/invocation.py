# Copyright: see copyright.txt
from symbolic.symbolic_types.symbolic_int import SymbolicInteger
from symbolic.symbolic_types.symbolic_str import SymbolicStr
from itertools import product


class FunctionInvocation:
	def __init__(self, function, reset):
		self.function = function
		self.reset = reset
		self.arg_constructor = {}
		self.initial_value = {}
		self.unfixed_args = []
		self.unfixed_args_assignment_iter = None
		self.num_seed_assignments = 0

	def callFunction(self,args):
		self.reset()
		return self.function(**args)

	def addArgumentConstructor(self, name, init, constructor):
		self.initial_value[name] = init
		self.arg_constructor[name] = constructor

	def addUnfixedArgument(self, name):
		self.unfixed_args.append(name)

	# Solver -> Pairs of value + symbolic type
	_INTEGER_SEEDS = [(0, SymbolicInteger), (1, SymbolicInteger), (-1, SymbolicInteger)]
	_STRING_SEEDS = [("", SymbolicStr), ("A", SymbolicStr)]
	_SEED_VALUES = {	"z3": _INTEGER_SEEDS,
						"cvc": _STRING_SEEDS + _INTEGER_SEEDS
				   }

	def initializeArgumentAssignmentIter(self, solver):
		if self.unfixed_args_assignment_iter is None:
			seeds = FunctionInvocation._SEED_VALUES[solver]
			num_args = len(self.unfixed_args)
			self.unfixed_args_assignment_iter = product(seeds, repeat=num_args)
			self.num_seed_assignments = len(seeds)**num_args

	def has_remaining_seeds(self):
		self.unfixed_args_assignment_iter.has_next()

	def initializeUnfixedArguments(self, solver):
		self.initializeArgumentAssignmentIter(solver)

		values_with_constructors = self.unfixed_args_assignment_iter.__next__()
		assert(len(self.unfixed_args) == len(values_with_constructors))

		for name, value_and_constructor in zip(self.unfixed_args, values_with_constructors):
			value = value_and_constructor[0]
			constructor = value_and_constructor[1]
			self.addArgumentConstructor(name, value, constructor)

	def getNames(self):
		return self.arg_constructor.keys()

	def createArgumentValue(self,name,val=None):
		if val == None:
			val = self.initial_value[name]
		return self.arg_constructor[name](name,val)

	

