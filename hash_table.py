class Node:
    def __init__(self, data=None, nex_node=None):
        self.data = data
        self.nex_node = nex_node

class Data:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class HashTable:
    def __init__(self, table_size):
        self.table_size = table_size
        self.hash_table = [None] * table_size
    
    def custome_hash(self, key):
        hash_value = 0
        for i in key:
            hash_value += ord(i)
            hash_value = (hash_value * ord(i)) % self.table_size
        return hash_value
    
    def add_key_value(self, key, value):
        hashed_key = self.custome_hash(key)
        if self.hash_table[hashed_key] is None:
            self.hash_table[hashed_key] = Node(Data(key, value), None)
        else:
            node = self.hash_table[hashed_key]
            while node.nex_node:
                node = node.nex_node
            node.nex_node = Node(Data(key, value), None)

    def get_value(self, key):
        hashed_key = self.custome_hash(key)
        if self.hash_table[hashed_key] is not None:
            node = self.hash_table[hashed_key]
            if node.nex_node is None:
                return node.data.value
            while node.nex_node:
                if key == node.data.key:
                    return node.data.value
                node = node.nex_node
            if key == node.data.key:
                return node.data.value
        return None
    
    def print_table(self):
        print("{")
        for i, value in enumerate(self.hash_table):
            if value is not None:
                linked_list_str = ""
                node = value
                if node.nex_node:
                    while node.nex_node:
                        linked_list_str += (str(node.data.key) + " : " + str(node.data.value) + " --> ")
                        node = node.nex_node
                    linked_list_str += (str(node.data.key) + " : " + str(node.data.value) + " --> None")
                    print(f'    [{i}] {linked_list_str}')
                else:
                    print(f'    [{i}] {value.data.key} : {value.data.value}')
            else:
                print(f'    [{i}] {value}')
        print("}")