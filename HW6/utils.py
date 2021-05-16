import numpy as np


''' Problem 1'''

class BinHeap:
    def __init__(self):
        self.heap_list = [0]
        self.current_size = 0
    
    def __len__(self):
        return len(self.heap_list)-1
    
    def perc_up(self, i): 
        while i // 2 > 0:
            if self.heap_list[i] < self.heap_list[i // 2]: 
                tmp = self.heap_list[i // 2] 
                self.heap_list[i // 2] = self.heap_list[i] 
                self.heap_list[i] = tmp
            i = i // 2            
            
    def insert(self, k): 
        self.heap_list.append(k) 
        self.current_size = self.current_size + 1 
        self.perc_up(self.current_size)      
        
    def perc_down(self, i):
        while (i * 2) <= self.current_size:
            mc = self.min_child(i)
            if self.heap_list[i] > self.heap_list[mc]:
                tmp = self.heap_list[i]
                self.heap_list[i] = self.heap_list[mc]
                self.heap_list[mc] = tmp
            i = mc
            
    def min_child(self, i):
        if i * 2 + 1 > self.current_size: 
            return i * 2
        else:
            if self.heap_list[i * 2] < self.heap_list[i * 2 + 1]:
                return i * 2 
            else:
                return i * 2 + 1        
            
    def del_min(self):
        ret_val = self.heap_list[1] 
        self.heap_list[1] = self.heap_list[self.current_size] 
        self.current_size = self.current_size - 1 
        self.heap_list.pop()
        self.perc_down(1)
        return ret_val
    
def post_encoding_processing(encoded_img):
    padded_encoded_img = padding_to_byte(encoded_img)
    byte_encoded_img = get_byte_array(padded_encoded_img)
    return byte_encoded_img


def padding_to_byte(encoded_img):
    extra_padding = 8 - len(encoded_img) % 8
    for i in range(extra_padding):
        encoded_img += "0"

    padded_info = "{0:08b}".format(extra_padding)
    encoded_img = padded_info + encoded_img
    return encoded_img

def get_byte_array(padded_encoded_img):
    if(len(padded_encoded_img) % 8 != 0):
        print("Encoded text not padded properly")
        exit(0)

    b = []
    for i in range(0, len(padded_encoded_img), 8):
        byte = padded_encoded_img[i:i+8]
        b.append(int(byte, 2))
    return np.array(b, dtype=np.uint8)



def pre_decoding_processing(byte_encoded_img):
    return remove_padding(byte_encoded_img)

def remove_padding(byte_encoded_img):
    bit_string = ""
    for byte in byte_encoded_img:
        bits = bin(byte)[2:].rjust(8, '0')
        bit_string += bits

    padded_info = bit_string[:8]
    extra_padding = int(padded_info, 2)

    bit_string = bit_string[8:] 
    encoded_img = bit_string[:-1*extra_padding]

    return encoded_img


''' Problem 2'''

# Completed TreeNode class
class TreeNode:
    def __init__(self, key, val, left = None, right = None, parent = None):
        self.key = key
        self.payload = val
        self.left_child = left
        self.right_child = right
        self.parent = parent
        
    def has_left_child(self): 
        return self.left_child
    
    def has_right_child(self): 
        return self.right_child
    
    def is_left_child(self):
        return self.parent and self.parent.left_child == self
    
    def is_right_child(self):
        return self.parent and self.parent.right_child == self
    
    def is_root(self):
        return not self.parent
    
    def is_leaf(self):
        return not (self.right_child or self.left_child)
    
    def has_any_children(self):
        return self.right_child or self.left_child
    
    def has_both_children(self):
        return self.right_child and self.left_child
    
    def replace_node_data(self, key, value, lc, rc): 
        self.key = key 
        self.payload = value 
        self.left_child = lc 
        self.right_child = rc
        if self.has_left_child():
            self.left_child.parent = self 
        if self.has_right_child():
            self.right_child.parent = self
            
    def splice_out(self):
        if self.is_leaf():
            if self.is_left_child():
                self.parent.left_child = None
            else:
                self.parent.right_child = None
        elif self.has_any_children():
            if self.has_left_child():
                if self.is_left_child():
                    self.parent.left_child = self.left_child
                else:
                    self.parent.right_child = self.left_child
                self.left_child.parent = self.parent
            else:
                if self.is_left_child():
                    self.parent.left_child = self.right_child
                else:
                    self.parent.right_child = self.right_child
                self.right_child.parent = self.parent
        
    def find_successor(self):
        succ = self.right_child.find_min() 
        return succ
    
    def find_min(self): 
        current = self
        while current.has_left_child(): 
            current = current.left_child
        return current         
            
    def __iter__(self):
        if self:
            if self.has_left_child():
                for elem in self.left_child:
                    yield elem
            yield self.key
            if self.has_right_child():
                for elem in self.right_child:
                    yield elem
                    
                    
# Basic BinarySearchTree class 
class BinarySearchTree: 
    def __init__(self):
        self.root = None
        self.size = 0
        
    def length(self): 
        return self.size
    
    def __len__(self): 
        return self.size
    
    def __iter__(self):
        return self.root.__iter__()
    
    def put(self, key, val): 
        if self.root:
            self._put(key, val, self.root) 
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1
        
    def _put(self, key, val, current_node): 
        if key < current_node.key:
            if current_node.has_left_child(): 
                self._put(key, val, current_node.left_child) 
            else:
                current_node.left_child = TreeNode(key, val, parent=current_node)
        else:
            if current_node.has_right_child():
                self._put(key, val, current_node.right_child)
            else:
                current_node.right_child = TreeNode(key, val, parent=current_node)        
                
    def __setitem__(self, k, v): 
        self.put(k, v)                
        
    def get(self,key): 
        if self.root:
            res = self._get(key, self.root) 
            if res:
                return res.payload 
            else:
                return None 
        else:                        
            return None        
    
    def _get(self, key, current_node): 
        if not current_node:
            return None
        elif current_node.key == key:
            return current_node 
        elif key < current_node.key:
            return self._get(key, current_node.left_child) 
        else:
            return self._get(key, current_node.right_child)    
        
    def __getitem__(self, key): 
        return self.get(key)            
    
    def __contains__(self, key):
        if self._get(key, self.root):
            return True 
        else:
            return False
        
    def delete(self, key): 
        if self.size > 1:
            node_to_remove = self._get(key, self.root) 
            if node_to_remove:
                self.remove(node_to_remove)
                self.size = self.size - 1 
            else:
                raise KeyError('Error, key not in tree') 
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1 
        else:
            raise KeyError('Error, key not in tree')
            
    def __delitem__(self, key): 
        self.delete(key)            
        
    def remove(self, current_node):      
        if current_node.is_leaf():
            if current_node == current_node.parent.left_child:
                current_node.parent.left_child = None
            else:
                current_node.parent.right_child = None
                
        elif current_node.has_both_children():
            succ = current_node.find_successor() 
            succ.splice_out()
            current_node.key = succ.key 
            current_node.payload = succ.payload    
            
        else: # this node has one child
            if current_node.has_left_child():
                if current_node.is_left_child(): 
                    current_node.left_child.parent = current_node.parent 
                    current_node.parent.left_child = current_node.left_child 
                    
                elif current_node.is_right_child():
                    current_node.left_child.parent = current_node.parent
                    current_node.parent.right_child = current_node.left_child
                    
                else: 
                    current_node.replace_node_data(
                      current_node.left_child.key,
                      current_node.left_child.payload,
                      current_node.left_child.left_child,
                      current_node.left_child.right_child)       
                    
            else:
                if current_node.is_left_child():
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.left_child = current_node.right_child
                    
                elif current_node.is_right_child(): 
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.right_child = current_node.right_child
                    
                else: 
                    current_node.replace_node_data(
                      current_node.right_child.key,
                      current_node.right_child.payload,
                      current_node.right_child.left_child,
                      current_node.right_child.right_child)
                    
def print_tree(tree_node, level=0):
    if isinstance(tree_node,BinarySearchTree):
        print('----- Printing tree structure -----')
        print('Total Nodes : ', len(tree_node))
        tree_node = tree_node.root
        print('(Root) [{:2d}]'.format(tree_node.key) + ':' + str(tree_node.payload))
    if tree_node == None:
        return
    if level != 0:
        print("     "*level, end='')
        if tree_node.parent.left_child == tree_node:
            print('{:2d}-(L) [{:2d}]:'.format(level, tree_node.key) + str(tree_node.payload))
        else:
            print('{:2d}-(R) [{:2d}]:'.format(level, tree_node.key) + str(tree_node.payload))
    print_tree(tree_node.right_child,level+1)
    print_tree(tree_node.left_child,level+1)