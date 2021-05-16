# DO NOT modify this code
class HashTable:
    def __init__(self, size):
        self.size = size
        self.__slots = [None] * self.size
        self.__data = [None] * self.size
        
    def hash_func(self, key):
        return key % self.size
    
    def rehash_func(self, key, cnt):
        return (key + cnt ** 2) % self.size
        
    def put(self, key, data):
        hash_value = self.hash_func(key)
        
        if self.__slots[hash_value] == None:
            self.__slots[hash_value] = key
            self.__data[hash_value] = data
        else:
            if self.__slots[hash_value] == key:
                self.__data[hash_value] = data
            else:
                cnt = 1
                next_slot = self.rehash_func(hash_value, cnt)
                while self.__slots[next_slot] != None and self.__slots[next_slot] != key:
                    cnt += 1
                    next_slot = self.rehash_func(hash_value, cnt)
                    
                if self.__slots[next_slot] == None:
                    self.__slots[next_slot] = key
                    self.__data[next_slot] = data
                    
                else:
                    self.__data[next_slot] = data
                    
    def get(self, key):
        start_slot = self.hash_func(key)
        data = None
        stop = False
        found = False
        position = start_slot
        cnt = 1
        while self.__slots[position] != None and not found and not stop:
            if self.__slots[position] == key:
                found = True
                data = self.__data[position]
            else:
                position = self.rehash_func(key, cnt)
                if position == start_slot:
                    stop = True
                cnt += 1
        return data
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, data):
        self.put(key, data)