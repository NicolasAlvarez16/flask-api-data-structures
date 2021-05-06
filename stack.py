class Node:
    def __init__(self, data, nex_node):
        self.data = data
        self.nex_node = nex_node

class Stack:
    def __init__(self):
        self.top = None
    
    def peek(self):
        return self.top

    def push(self, data):
        next_node = self.top
        new_top = Node(data, next_node)
        self.top = new_top
    
    def pop(self):
        if self.top is None:
            return None
        removed = self.top
        self.top = self.top.nex_node
        return removed