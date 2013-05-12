# -----------------------------------------------------------------------------
# stack.py
# Stack used in the indent filter.
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------


class EmptyStackException(Exception):
    pass


class Node:
    def __init__(self, value, next):
        self.value = value
        self.next = next


class Stack:
    def __init__(self):
        self.head = None

    def __iter__(self):
        return self

    def __str__(self):
        return 'top is ', self.read()

    def next(self):
        next_node = self.head
        while next_node is not None:
            yield next_node
            next_node = next_node.next
        raise StopIteration

    def empty(self):
        """
         Returns True if node is empty
        """
        return self.head is None

    def push(self, element):
        self.head = Node(element, self.head)

    def read(self):
        """
        Returns the value of the last element on the stack.
        Raises:
         EmptyStackException
        """
        if self.empty():
            raise EmptyStackException
        return self.head.value

    def pop(self):
        """
        Pops the last element of the stack.
        Raises:
         EmptyStackException
        """
        result = self.read()
        self.head = self.head.next
        return result

# test
