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


class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.storage = [[] for i in range(self.capacity)]

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
        return hash & 0xffffffff

    def hash_index(self, key):
        # Take an arbitrary key and return a valid integer index
        # between within the storage capacity of the hash table.
        #
        # return self.fnv1(key) % self.capacity
        # return self.fnv1_64(key) % self.capacity # <- not working
        return self.djb2(key) % self.capacity

    # Allow collisions
    # def put(self, key, value):
    #     # Store the value with the given key.
    #     # Hash collisions should be handled with Linked List Chaining.
    #     # Implement this.
    #     self.storage[self.hash_index(key)] = value

    # Avoiding collisions
    def put(self, key, value):
        h = self.storage[self.hash_index(key)]
        if h:
            self.storage[self.hash_index(key)].add(key, value)
        else:
            self.storage[self.hash_index(key)] = HashedLinkedList()
            self.storage[self.hash_index(key)].add(key, value)

    # Allow collisions
    # def delete(self, key):
    #     # Remove the value stored with the given key.
    #     # Print a warning if the key is not found.
    #     # Implement this.
    #     if self.storage[self.hash_index(key)]:
    #         self.storage[self.hash_index(key)] = None
    #     else:
    #         print("Key not found")

    # Avoiding collisions
    def delete(self, key):
        if self.storage[self.hash_index(key)]:
            self.storage[self.hash_index(key)].delete(key)
        else:
            print("Key not found")

    # Allow collisions
    # def get(self, key):
    #     # Retrieve the value stored with the given key.
    #     # Returns None if the key is not found.
    #     # Implement this.
    #     if self.storage[self.hash_index(key)]:
    #         return self.storage[self.hash_index(key)]
    #     else:
    #         return None

    # Avoiding collisions
    def get(self, key):
        h = self.storage[self.hash_index(key)]
        if h:
            return h.find(key)
        else:
            return None

    def resize(self):
        # Doubles the capacity of the hash table and
        # rehash all key/value pairs.
        # Implement this.
        pass


if __name__ == "__main__":
    ht = HashTable(2)

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
    ht.resize()
    new_capacity = len(ht.storage)

    # print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    print("")
