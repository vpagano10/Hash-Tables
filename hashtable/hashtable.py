class HashTableEntry:
    # Hash Table entry, as a linked list node.
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashedLinkedList:
    def __init__(self):
        self.head = None

    def add(self, key, value):
        new_node = HashTableEntry(key, value)
        new_node.next = self.head
        self.head = new_node

    def find(self, key):
        current = self.head
        while current:
            if current.key == key:
                return current.value
            current = current.next

    def find_and_replace(self, key, _value):
        current = self.head
        while current:
            if current.key == key:
                current.value = _value
            current = current.next

    def delete(self, key):
        if key == self.head.key:
            self.head = self.head.next
        current = self.head
        prev = None
        while current:
            if current.key == key:
                prev.next = current.next
            prev = current
            current = current.next

    def print_all_nodes(self):
        current = self.head
        while current:
            print(current.value)
            current = current.next

    def all_nodes(self):
        current = self.head
        arr = []
        while current:
            arr.append(current)
            current = current.next
        return arr


class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.storage = [[] for i in range(self.capacity)]
        self.load = 0

    # 32-bit hash
    def fnv1(self, key):
        hval = 0x811c9dc5
        fnv_32_prime = 0x01000193
        unit_32_max = 2**32
        for i in key:
            hval = hval ^ ord(i)
            hval = (hval * fnv_32_prime) % unit_32_max
        return hval

    # 64-bit hash
    def fnv1_64(self, key):
        str_bytes = str(key).encode()
        FNV_offset_basis = 14695981039346656037
        FNV_prime = 1099511628211
        hash = FNV_offset_basis
        for byte in str_bytes:
            hash = hash * FNV_prime
            hash = hash ^ byte
        hash &= 0xffffffffffffffff
        return hash

    def djb2(self, key):
        hash = 5381
        for i in key:
            hash = ((hash << 5) + hash) + ord(i)
        # hash = hash % slef.capacity
        return hash & 0xffffffff

    def load_balance(self):
        return self.load / self.capacity

    def hash_index(self, key):
        # return self.fnv1(key) % self.capacity
        # return self.fnv1_64(key) % self.capacity # <- not working
        return self.djb2(key) % self.capacity

    # Avoiding collisions
    def put(self, key, value):
        index = self.hash_index(key)
        if self.storage[index]:
            if self.storage[index].find(key):
                self.storage[index].find_and_replace(key, value)
            else:
                self.storage[index].add(key, value)
                self.load += 1
        else:
            self.storage[index] = HashedLinkedList()
            self.storage[index].add(key, value)
            self.load += 1
        if self.load_balance() > 0.7:
            self.resize()

    # Avoiding collisions
    def delete(self, key):
        index = self.hash_index(key)
        if self.storage[index].find(key):
            self.storage[index].delete(key)
            self.load -= 1
        if self.load_balance() < 0.2 and self.capacity > 8:
            self.resize()

    # Avoiding collisions
    def get(self, key):
        h = self.storage[self.hash_index(key)]
        if h:
            return h.find(key)
        else:
            return None

    def resize(self):
        nodes = []
        if self.load_balance() > 0.7:
            for i in range(self.capacity):
                if self.storage[i]:
                    nodes += self.storage[i].all_nodes()
            self.capacity = self.capacity * 2
            new_storage = [[] for i in range(self.capacity)]
            self.storage = new_storage
            self.load = 0
            for node in nodes:
                self.put(node.key, node.value)
        elif self.load_balance() < 0.2 and self.capacity > 8:
            for i in range(self.capacity):
                if self.storage[i]:
                    nodes += self.storage[i].all_nodes()
            self.capacity = self.capacity // 2
            new_storage = [[] for i in range(self.capacity)]
            self.storage = new_storage
            self.load = 0
            for node in nodes:
                self.put(node.key, node.value)


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "Tiny hash table")
    ht.put("line_2", "Filled beyond capacity")
    ht.put("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.put("line_4", "Linked list saves the day!")
    ht.put("line_5", "Linked list saves the day!")
    ht.put("line_6", "Linked list saves the day!")
    ht.put("line_7", "Linked list saves the day!")
    ht.put("line_8", "Linked list saves the day!")
    ht.put("line_9", "Linked list saves the day!")
    ht.resize()
    new_capacity = len(ht.storage)
    ht.delete("line_4")
    ht.delete("line_5")
    ht.delete("line_6")
    ht.delete("line_7")
    ht.delete("line_8")
    ht.delete("line_9")
    ht.resize()
    last_capacity = len(ht.storage)

    print(
        f"\nResized from {old_capacity} to {new_capacity} ended {last_capacity}.\n")

    # Test if data intact after resizing
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    print("")
