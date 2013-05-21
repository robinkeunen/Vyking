from src import ast
from src.misc import add_to_class, trace
from src.type_checking import Environment

    @trace

    @add_to_class(ast.Statement_sequence)
    def type_check(self, **kw):
        entry_point = kw.pop('entry_point', False)
        if entry_point:
            self.environment = Environment()
        else:
            self.set_environment(**kw)