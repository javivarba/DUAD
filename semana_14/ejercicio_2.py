
class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class Deque:
    def __init__(self):
        self.head = None
        self.tail = None

    def push_left(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def push_right(self, value):
        new_node = Node(value)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def pop_left(self):
        if self.head is None:
            print("Deque is empty.")
            return None
        popped_value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        return popped_value

    def pop_right(self):
        if self.tail is None:
            print("Deque is empty.")
            return None
        popped_value = self.tail.value
        self.tail = self.tail.prev
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        return popped_value

    def print_deque(self):
        current = self.head
        while current is not None:
            print(current.value)
            current = current.next

# To Test
deque = Deque()
deque.push_right(10)
deque.push_right(20)
deque.push_left(5)
deque.push_left(1)
deque.print_deque()
print("Pop left:", deque.pop_left())
print("Pop right:", deque.pop_right())
deque.print_deque()
