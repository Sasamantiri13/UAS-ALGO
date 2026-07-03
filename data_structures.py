class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def remove_by_condition(self, condition_func):
        """Menghapus node berdasarkan fungsi kondisi (misal: NIM match)."""
        current = self.head
        removed = False
        while current:
            if condition_func(current.data):
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                
                self.size -= 1
                removed = True
                # Kita asumsikan NIM unik, jadi bisa break setelah ketemu satu
                break
            current = current.next
        return removed

    def to_list(self):
        """Konversi ke list Python untuk kompatibilitas dengan UI/Sorting."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def from_list(self, data_list):
        """Membangun Linked List dari list Python."""
        self.head = self.tail = None
        self.size = 0
        for item in data_list:
            self.append(item)

# Simple Cache Implementation for Search
class SearchCache:
    def __init__(self, max_size=10):
        self.cache = {}
        self.max_size = max_size
        self.order = []

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.max_size:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)

    def clear(self):
        self.cache.clear()
        self.order.clear()
