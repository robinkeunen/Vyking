__author__ = 'Robin Keunen'

#import src.visit as visit
import src.ast as ast

#
# class AbstractSyntaxTreeVisitor(object):
#
#     @visit.on('node')
#     def visit(self, node):
#         """
#         This is the generic method that initializes the
#         dynamic dispatcher.
#         """
#
#     @visit.when(ast.ASTNode)
#     def visit(self, node):
#         """
#         Will run for nodes that do specifically match the
#         provided type.
#         """
#         print("Unrecognized node:", node)
#
#     @visit.when(ast.AssignmentExpression)
#     def visit(self, node):
#         """ Matches nodes of type AssignmentExpression. """
#         node.children[0].accept(self)
#         print('=')
#         node.children[1].accept(self)
#
#     @visit.when(ast.VariableNode)
#     def visit(self, node):
#         """ Matches nodes that contain variables. """
#         print(node.name)
#
#     @visit.when(ast.Literal)
#     def visit(self, node):
#         """ Matches nodes that contain literal values. """
#         print(node.value)

