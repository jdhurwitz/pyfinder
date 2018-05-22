# used to do AST rewrites.
import ast
from pprint import pprint

import inspect

# sample command:
# python pyexz3.py pyfinder_tests/custom_tests/cvc/string_startswith3.py  --cvc
# Ideally: we want to identify
class ASTRewriter:
    def __init__(self):
        pass

    def rewrite(self, func):
        src_str = inspect.getsource(func)
        root = ast.parse(src_str)
        print("Full ast dump")
        print(ast.dump(root))
        print("-"*10)
        print("AST dump with non-annotated fields, theoretically 'executable' code")
        print(ast.dump(root, annotate_fields=False))
        print("-"*10)
        print("Visited?")
        self.SymbolicWrapper().visit(root)
        print("-"*10)
        return func

    # useful(?) resource: https://eli.thegreenplace.net/2009/11/28/python-internals-working-with-python-asts
    class SymbolicWrapper(ast.NodeTransformer):
        def visit(self, node):
            # visit children first
            self.generic_visit(node)
            if (isinstance(node, ast.Str)):
                print("HI")
                print(ast.dump(node, annotate_fields=False))
                # Partial progress: need to replace this with a call to symbolic string
                # also add other types as needed.
                
            return node
