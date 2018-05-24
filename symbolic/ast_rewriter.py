# used to do AST rewrites.
import ast
from pprint import pprint

import inspect

# sample command:
# python pyexz3.py pyfinder_tests/custom_tests/cvc/string_startswith3.py  --cvc
# TODO: check and redefine other function calls as needed, eg non_entry_function_call.py
# Approach: recursively visit AST and call rewrite on Name(<non-symbolic-type>), Load()).
# What do we do if this is actually a variable as opposed to a function? Need to wrap that too...
from symbolic.symbolic_types import SymbolicType, SymbolicStr

# Strongly recommend https://greentreesnakes.readthedocs.io/en/latest/ for
# using the AST library
class ASTRewriter:
    def __init__(self):
        pass
    # functions we need to import, and also avoid rewriting
    import symbolic.symbolic_types as pyfinder_symbolic_types
    pyfinder_symbolic_dict = pyfinder_symbolic_types.__dict__


    def rewrite(self, entryPoint, global_namespace):
        global_namespace.update(self.__class__.pyfinder_symbolic_dict)
        return self._rewrite(entryPoint, global_namespace, {})

    def _rewrite(self, entryPoint, global_namespace, local_namespace):
        func = global_namespace[entryPoint]
        src_str = inspect.getsource(func)
        # print(src_str)
        root = ast.parse(src_str)
        # print("Full ast dump")
        # print(ast.dump(root))
        # print("-"*10)
        # print("AST dump with non-annotated fields, theoretically 'executable' code")
        # print(ast.dump(root, annotate_fields=False))
        # print("-"*10)

        # Rewrite ASTs for nested function calls - currently incomplete and not supported.
        # self.FunctionDefRewriter(global_namespace, local_namespace).visit(root)

        # Wrap program literals (eg string constants) with symbolic types that
        # evaluate as concrete values, but otherwise track symbolic execution for
        # supported functions.
        self.ProgramLiteralWrapper().visit(root)


        # no longer required, but retained in case it's useful later.
        # self.FunctionDefRenamer().visit(root)

        # needed if you generate new nodes without using ast.copy_location or otherwise properly setting ast props.
        ast.fix_missing_locations(root)
        # print("-"*10)
        # print(ast.dump(root, annotate_fields=False))

        # this will define the entryPoint function within the new dictionary
        # jteoh: not 100% sure this is required, but it helps prevent potential conflicts anyways?
        # we also need to ensure that the symbolic data types we're using are imported within the namespace,
        # since we rewrite the program to use them. For unknown reasons, pyexz3 reimports the file cleanly
        # each time, so we also need to re-import our symbolic types each time.
        exec(compile(root, filename="<ast>", mode="exec"), global_namespace, local_namespace)

        # alt: write an expression ast to get this function
        return local_namespace[entryPoint]
        # return func

    # useful(?) resource: https://eli.thegreenplace.net/2009/11/28/python-internals-working-with-python-asts
    # This technically wraps all constants, including those in decorators.
    # The resulting SymbolicType is hardcoded to always evaluate as a concrete value, but still keep
    # track of the symbolic execution path. PyExZ3 will then additionally wrap any decorator
    # literal instances, meaning that in those symbolic/concrete instances the SymbolicType here is simply treated
    # as a literal (with a slight additional memory overhead of maintaining symbolic execution paths that are
    # unused).
    class ProgramLiteralWrapper(ast.NodeTransformer):
        CONCRETE_WRAPPER_STR = ast.Str(SymbolicType.CONCRETE_WRAPPER_NAME)
        def visit(self, node):
            # visit children first
            self.generic_visit(node)
            if (self.is_wrappable_type(node)):
                # print(ast.dump(node, annotate_fields=False))
                # Call takes 5 args:
                # func (in this case, the SymbolicType constructor)
                # args (in this case, fixed object name + the original string we want to wrap)
                # keywords, starargs, kwargs -> all empty for this usage.
                symbolic_classname = self.get_symbolic_class(node).__name__
                result = ast.Call(ast.Name(SymbolicStr.__name__, ast.Load()),
                                [self.CONCRETE_WRAPPER_STR, node],
                                [], None, None)
                # print(ast.dump(result, annotate_fields=False))
                return result
            else:
                return node

        def is_wrappable_type(self, node):
            # TODO add the others
            return isinstance(node, ast.Str)

        def get_symbolic_class(self, node):
            assert(self.is_wrappable_type(node))
            if isinstance(node, ast.Str):
                return SymbolicStr
            else:
                raise Exception("Wrappable constant type does not have corresponding symbolic class: " + str(type(node)))


    class FunctionDefRewriter(ast.NodeVisitor):
        """
        Incomplete class to rewrite nested function calls - presumably, this would call
        ASTRewriter.rewrite on referenced methods. In practice this is nontrivial and
        it's not even guaranteed that we can get source code for every method,
        so I'm abandoning this approach for now but leaving the class in case it
        becomes useful later.
        """
        def __init__(self, global_namespace, local_namespace):
            self.global_namespace = global_namespace
            self.local_namespace = local_namespace
            import symbolic.args as skip_lib
            self.skip_dict = skip_lib.__dict__

        def visit_Call(self, node):
            func_node = node.func
            print(ast.dump(func_node))
            if(isinstance(func_node, ast.Name)):
                func_id = node.func.id
                print("Skip?: " + str(func_id in self.skip_dict))
                print("Redefine?: " + str(func_id in self.global_namespace and func_id not in self.skip_dict))
            elif(isinstance(func_node, ast.Attribute)):
                # func_node.
                pass

