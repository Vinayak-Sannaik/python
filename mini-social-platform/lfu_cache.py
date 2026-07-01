from collections import defaultdict


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 1
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = Node(None, None)
        self.tail = Node(None, None)

        self.head.next = self.tail
        self.tail.prev = self.head

        self.size = 0

    def add_to_front(self, node):
        node.next = self.head.next
        node.prev = self.head

        self.head.next.prev = node
        self.head.next = node

        self.size += 1

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

        self.size -= 1

    def remove_last(self):
        if self.size == 0:
            return None

        node = self.tail.prev
        self.remove(node)
        return node


class LFUCache:

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than zero")

        self.capacity = capacity
        self.min_freq = 0

        self.nodes = {}
        self.freq_map = defaultdict(DoublyLinkedList)

    def _update_frequency(self, node):
        old_freq = node.freq

        self.freq_map[old_freq].remove(node)

        if old_freq == self.min_freq and self.freq_map[old_freq].size == 0:
            self.min_freq += 1

        node.freq += 1

        self.freq_map[node.freq].add_to_front(node)

    def get(self, key):
        if key not in self.nodes:
            return None

        node = self.nodes[key]
        self._update_frequency(node)

        return node.value

    def put(self, key, value):

        if key in self.nodes:
            node = self.nodes[key]
            node.value = value
            self._update_frequency(node)
            return

        if len(self.nodes) >= self.capacity:
            lfu_node = self.freq_map[self.min_freq].remove_last()
            del self.nodes[lfu_node.key]

        node = Node(key, value)

        self.nodes[key] = node

        self.min_freq = 1

        self.freq_map[1].add_to_front(node)

    def invalidate(self, key):
        if key not in self.nodes:
            return

        node = self.nodes[key]

        self.freq_map[node.freq].remove(node)

        del self.nodes[key]

        if self.min_freq == node.freq and self.freq_map[node.freq].size == 0:
            self.min_freq = 1