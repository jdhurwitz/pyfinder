# used to do AST rewrites.
import ast
from pprint import pprint

import inspect

# sample command:
# python pyexz3.py pyfinder_tests/custom_tests/cvc/string_startswith3.py  --cvc
# TODO: check and redefine other function calls as needed?
from symbolic.symbolic_types import SymbolicType, SymbolicStr


class ASTRewriter:
    def __init__(self):
        pass

    def rewrite(self, func, entryPoint, namespace):
        src_str = inspect.getsource(func)
        root = ast.parse(src_str)
        # print("Full ast dump")
        # print(ast.dump(root))
        # print("-"*10)
        # print("AST dump with non-annotated fields, theoretically 'executable' code")
        # print(ast.dump(root, annotate_fields=False))
        # print("-"*10)
        self.SymbolicWrapper().visit(root)

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
        import symbolic.symbolic_types as pyfinder_symbolic_types
        namespace.update(pyfinder_symbolic_types.__dict__) # todo: namespace should only be set up once
        newlocal = {}
        exec(compile(root, filename="<ast>", mode="exec"), namespace, newlocal)


        return newlocal[entryPoint]
        # return func

    # useful(?) resource: https://eli.thegreenplace.net/2009/11/28/python-internals-working-with-python-asts
    class SymbolicWrapper(ast.NodeTransformer):
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


    class FunctionDefRenamer(ast.NodeTransformer):
        """ Unused - useful if you want to rename function defs (which don't seem necessary here) """
        def visit_FunctionDef(self, node):
            node.name = "_pyfinder_" + node.name
            self.generic_visit(node)
            return node

