'''
The purpose of this file is to code a partially persistent
pointer machine
'''

import numpy as np


class PartialPointerMachine:
    def __init__(self, y=0, x=0):
        self.root = Node(version = 0)
        self.latest_node = root

    def mod(self, field_changed, value_changed):
        '''Provides modification for the partially persistent pointer machine'''
        self.latest_node = self.latest_node.mod(field, new_value)

    def read(self, field, version=self.latest_node.getVersion()):
        '''Performs read operations on the data structure'''
        if version > self.latest_node.getVersion():
            return self.latest_node.mods 

    def traverse(self, version):
        '''
        Traverse the nodes from the root node to the version number
        returns the latest node if the version is greater than the latest
        '''
        node = self.root
        if self.current_version < version:
            return self.latest_node
        
        while(node.getVersion() < version):
            node = node.getNext()
        return node
    

    
class Node:
    '''Define a Node class for use in a pointer machine'''
    def __init__(self, version, back_pointer=None, forward_pointer=None):
        self.back_pointers = back_pointer
        self.forward_pointer = forward_pointer
        self.version= version
        self.mods = np.empty(10, dtype=object)
        self.idx = 0

    def mod(self, field, new_value):
        '''Modify a field'''
        self.version += 1
        if self.idx != 10:
            self.mods[self.idx] = (self.version, field, new_value)
            self.idx += 1
            return self
        else:
            new_node = Node(self.version, back_pointer = self, forward_pointer = None)
            new_node.mods[0] = (self.version, field, new_value)
            new_node.idx += 1
            return new_node

    def getNext(self):
        '''returns the next pointer'''
        return self.forward_pointer

    def getVersion(self): 
        return self.version

    def getFieldValue(self, field, version):
        '''Gets a field value based on version'''
        fields = [mod[1] for mod in self.mods if mod is not None]
        # get the index based on the given version
        return self.mods[version - self.mods[0][0]]