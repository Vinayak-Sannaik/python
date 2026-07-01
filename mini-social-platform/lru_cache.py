class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than zero")

        self.capacity = capacity
        self.cache = {}

        # Dummy nodes
        self.head = Node()
        self.tail = Node()

        self.head.next = self.tail
        self.tail.prev = self.head

    # -------------------------
    # Doubly Linked List Helpers
    # -------------------------

    def _add_to_front(self, node):
        node.next = self.head.next
        node.prev = self.head

        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_front(self, node):
        self._remove_node(node)
        self._add_to_front(node)

    def _remove_lru(self):
        lru = self.tail.prev

        self._remove_node(lru)

        del self.cache[lru.key]

    # -------------------------
    # Public APIs
    # -------------------------

    def get(self, key):
        if key not in self.cache:
            return None

        node = self.cache[key]
        self._move_to_front(node)

        return node.value

    def put(self, key, value):

        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_front(node)
            return

        node = Node(key, value)

        self.cache[key] = node
        self._add_to_front(node)

        if len(self.cache) > self.capacity:
            self._remove_lru()

    def invalidate(self, key):
        if key not in self.cache:
            return

        node = self.cache[key]

        self._remove_node(node)

        del self.cache[key]

    # Helper for testing
    def keys(self):
        result = []

        curr = self.head.next

        while curr != self.tail:
            result.append(curr.key)
            curr = curr.next

        return result