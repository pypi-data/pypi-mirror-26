import ast

from .operator import Operator


class ZeroIterationLoop(Operator):
    """An operator that modified for-loops to have zero iterations."""

    def visit_For(self, node):  # noqa
        return self.visit_mutation_site(node)

    def mutate(self, node, _):
        """Modify the For loop to evaluate to None"""
        empty_list_node = ast.List(elts=[], ctx=ast.Load())
        new_node = ast.For(node.target, empty_list_node, node.body,
                           node.orelse)
        return new_node
