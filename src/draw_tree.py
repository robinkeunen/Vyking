from src import pydot

__author__ = 'Robin Keunen'

from src.misc import add_to_class
import src.ast as ast


@add_to_class(ast.Statement_sequence)
def make_tree_graph(self, dot=None, edgeLabels=True):
    """
        Makes a dot object to write subtree to output
        """

    children = self.get_children()
    if not dot:
        m_dot = pydot.Dot()
    else:
        m_dot = dot

    # if len(children) == 1 and (dot is not None):
    #     children[0].make_tree_graph(dot=m_dot, edgeLabels=edgeLabels)
    #     edge = pydot.Edge(self.id, children[0].id)
    #     m_dot.add_edge(edge)
    #     return m_dot

    m_dot.add_node(pydot.Node(self.id, label=self.type))
    label = edgeLabels and len(children) - 1

    for i, c in enumerate(children):
        if issubclass(c.__class__, ast.ASTNode):
            c.make_tree_graph(dot=m_dot, edgeLabels=edgeLabels)
            edge = pydot.Edge(self.id, c.id)
            if label:
                edge.set_label(str(i))
            m_dot.add_edge(edge)
    return m_dot


@add_to_class(ast.Expression)
def make_tree_graph(self, dot=None, edgeLabels=True):
    """
        Makes a dot object to write subtree to output
        """
    if not dot: dot = pydot.Dot()
    dot.add_node(pydot.Node(self.id, label=self.op))
    label = edgeLabels and len(self.get_children()) - 1

    for i, c in enumerate(self.get_children()):
        if issubclass(c.__class__, ast.ASTNode):
            c.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
            edge = pydot.Edge(self.id, c.id)
            if label:
                edge.set_label(str(i))
            dot.add_edge(edge)
    return dot


@add_to_class(ast.Clause)
def make_tree_graph(self, dot=None, edgeLabels=True):
    """
        Makes a dot object to write subtree to output
        """
    if not dot: dot = pydot.Dot()
    dot.add_node(pydot.Node(self.id, label=self.op))
    label = edgeLabels and len(self.get_children()) - 1

    for i, c in enumerate(self.get_children()):
        if issubclass(c.__class__, ast.ASTNode):
            c.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
            edge = pydot.Edge(self.id, c.id)
            if label:
                edge.set_label(str(i))
            dot.add_edge(edge)
    return dot


@add_to_class(ast.Fundef)
def make_tree_graph(self, dot=None, edgeLabels=True):
    """
        Makes a dot object to write subtree to output
        """
    if not dot: dot = pydot.Dot()
    dot.add_node(pydot.Node(self.id, label=self.type))
    label = edgeLabels and len(self.get_children()) - 1

    self.name.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
    edge = pydot.Edge(self.id, self.name.id)
    if label:
        edge.set_label(str(0))
        dot.add_edge(edge)

    for i, c in enumerate(self.parameters):
        if issubclass(c.__class__, ast.ASTNode):
            c.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
            edge = pydot.Edge(self.id, c.id)
            if label:
                edge.set_label(str(i))
            dot.add_edge(edge)

    self.suite.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
    edge = pydot.Edge(self.id, self.suite.id)
    if label:
        edge.set_label(str(0))
        dot.add_edge(edge)


    return dot


@add_to_class(ast.Funcall)
def make_tree_graph(self, dot=None, edgeLabels=True):
    """
        Makes a dot object to write subtree to output
        """
    if not dot: dot = pydot.Dot()
    dot.add_node(pydot.Node(self.id, label=self.type))
    label = edgeLabels and len(self.get_children()) - 1

    self.name.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
    edge = pydot.Edge(self.id, self.name.id)
    if label:
        edge.set_label(str(0))
        dot.add_edge(edge)

    for i, c in enumerate(self.args):
        if issubclass(c.__class__, ast.ASTNode):
            c.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
            edge = pydot.Edge(self.id, c.id)
            if label:
                edge.set_label(str(i))
            dot.add_edge(edge)
    return dot


@add_to_class(ast.Assignment)
def make_tree_graph(self, dot=None, edgeLabels=True):
    """
        Makes a dot object to write subtree to output
        """
    if not dot: dot = pydot.Dot()
    dot.add_node(pydot.Node(self.id, label=self.type))
    label = edgeLabels and len(self.get_children()) - 1

    self.name.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
    edge = pydot.Edge(self.id, self.name.id)
    if label:
        edge.set_label(str(0))
        dot.add_edge(edge)

    self.right.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
    edge = pydot.Edge(self.id, self.right.id)
    if label:
        edge.set_label(str(1))
        dot.add_edge(edge)

    return dot


@add_to_class(ast.ID)
def make_tree_graph(self, dot=None, edgeLabels=True):
    """
        Makes a dot object to write subtree to output
        """
    if not dot: dot = pydot.Dot()
    dot.add_node(pydot.Node(self.id, label=self.name))
    label = edgeLabels and len(self.get_children()) - 1

    for i, c in enumerate(self.get_children()):
        if issubclass(c.__class__, ast.ASTNode):
            c.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
            edge = pydot.Edge(self.id, c.id)
            if label:
                edge.set_label(str(i))
            dot.add_edge(edge)
    return dot


@add_to_class(ast.Vinteger)
def make_tree_graph(self, dot=None, edgeLabels=True):
    """
        Makes a dot object to write subtree to output
        """
    if not dot: dot = pydot.Dot()
    dot.add_node(pydot.Node(self.id, label=str(self.value)))
    label = edgeLabels and len(self.get_children()) - 1

    for i, c in enumerate(self.get_children()):
        if issubclass(c.__class__, ast.ASTNode):
            c.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
            edge = pydot.Edge(self.id, c.id)
            if label:
                edge.set_label(str(i))
            dot.add_edge(edge)
    return dot


@add_to_class(ast.Vfloat)
def make_tree_graph(self, dot=None, edgeLabels=True):
    """
        Makes a dot object to write subtree to output
        """
    if not dot: dot = pydot.Dot()
    dot.add_node(pydot.Node(self.id, label=str(self.value)))
    label = edgeLabels and len(self.get_children()) - 1

    for i, c in enumerate(self.get_children()):
        if issubclass(c.__class__, ast.ASTNode):
            c.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
            edge = pydot.Edge(self.id, c.id)
            if label:
                edge.set_label(str(i))
            dot.add_edge(edge)
    return dot


@add_to_class(ast.Vboolean)
def make_tree_graph(self, dot=None, edgeLabels=True):
    """
        Makes a dot object to write subtree to output
        """
    if not dot: dot = pydot.Dot()
    dot.add_node(pydot.Node(self.id, label=str(self.value)))
    label = edgeLabels and len(self.get_children()) - 1

    for i, c in enumerate(self.get_children()):
        if issubclass(c.__class__, ast.ASTNode):
            c.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
            edge = pydot.Edge(self.id, c.id)
            if label:
                edge.set_label(str(i))
            dot.add_edge(edge)
    return dot


@add_to_class(ast.Vstring)
def make_tree_graph(self, dot=None, edgeLabels=True):
    """
        Makes a dot object to write subtree to output
        """
    if not dot: dot = pydot.Dot()
    dot.add_node(pydot.Node(self.id, label=self.data))
    label = edgeLabels and len(self.get_children()) - 1

    for i, c in enumerate(self.get_children()):
        if issubclass(c.__class__, ast.ASTNode):
            c.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
            edge = pydot.Edge(self.id, c.id)
            if label:
                edge.set_label(str(i))
            dot.add_edge(edge)
    return dot

