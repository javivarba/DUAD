
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            print("Stack is empty.")
            return None
        popped_value = self.top.value
        self.top = self.top.next
        return popped_value

    def print_stack(self):
        current = self.top
        while current is not None:
            print(current.value)
            current = current.next

# To Test
stack = Stack()
stack.push(10)
stack.push(20)
stack.push(30)
stack.print_stack()
print("Popped:", stack.pop())
stack.print_stack()
