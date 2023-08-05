
import ast

import typed_ast.ast3

from .statically_typed import StaticallyTyped


def create_statically_typed_module(ast_module):

    class StaticallyTypedModuleClass(ast_module.Module, StaticallyTyped[ast_module]):

        #_type_fields = 'constants', 'classes', 'functions'
        _type_fields = 'classes', 'functions'

        def __init__(self, *args, **kwargs):
            #self._constants = {}
            self._classes = {}
            self._functions = {}
            super().__init__(*args, **kwargs)

        def _add_type_info(self):
            if not getattr(self, 'body', None):
                return
            classes, functions = {}, {}
            for node in self.body:
                if isinstance(node, ast_module.ClassDef):
                    classes[node.name] = node
                elif isinstance(node, ast_module.FunctionDef):
                    functions[node.name] = node
            self._classes, self._functions = classes, functions

    return StaticallyTypedModuleClass


StaticallyTypedModule = {ast_module: create_statically_typed_module(ast_module)
                         for ast_module in (ast, typed_ast.ast3)}
