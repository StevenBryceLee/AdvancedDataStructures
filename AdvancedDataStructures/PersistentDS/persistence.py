'''
This file is to follow along with session 1 of 
MIT advanced Data Structures: Persistent Data Structures
'''

import numpy as np
from numpy import array

'''
Definitions
------------------
Pointer machine
    A class or struct of pointers to other nodes. 
    Memory model
Operations
    x = new node
    x = y.field
    x.field = y
root node
    There is always a root node, and x and y are fields of the root
    You can always find a node via the root
Temporal DS
    -persistence: Where you don't forget anything
        If you make a change in the past, you get a different universe
Persistence:
    remember everything and keep all versions of data structures
    All DS operations are relative to a specified version
    An update makes and returns a new version
4 levels of persistence
    Partial persistence
        Only allowed to update the latest version, versions are ordered linearly
        This allows looking at past versions, but writes are not allowed
    Full persistence
        update any version
        The versions form a tree, through reference to a root
        not possible to merge versions
    confluent persistence
        possible to combine two versions which creates a new version
        Not possible to destroy versions
        The new versions form a directed acyclic graph
    functional persistence
        never modify any nodes, can only make new nodes
Partial persistence
    Any pointer-machine DS is accepted
    There must be a constant number of pointers into any node
    Any node can be made to be partially persistent with:
        O(1) amortized factor overhead
            O(1) space / change in DS
    Back pointers are stored, but only for latest version of DS
    modifications are stored as (version, field changed, value changed to)        
    A field read would require a field and version number, so you can see any past value
    a field modify (node.field = x):
        if node not full: add modification, increment version
        else: new node' with all mods, including latest mod
            New node will have an initially empty mod version
            update back pointers from node -> node'
            recursively update pointers
            prof: "I claim this is good"
potential method of amortization analysis
    c * sum(number of mods in latest version nodes)
    c is a constant factor
    When making a new node, since mods are empty, potential cost is low
amortized cost
    At most <= c + c + [-2cp + p * number of recursions]
    A constant time factor + cost if node not full + cost of changing pointers * cost of recursions
    -2cp term comes from cancelling the initial if condition cost, which occurs because you are counting that in recursions
    mind bending, since each recursion will cost 2c, the terms will cancel. Since that is the case, we have O(1)
Full persistence:
    Versions are now nodes on a tree, rather than a line
    To solve this, we linearlize the tree of versions
    We linearize by traversing the tree, which is done in linear time
        Based on his example, in order traversal, but probably fine to do any ordering
    We need to maintain the order of each subtree
    Using time travel, we take a DS from lecture 8 called an order-maintenance DS
            This is formally called a magical linked list
        You may insert an item before or after a given item in O(1)
        You may find the relative order of two items in the list in O(1)
            Is item X before or after item Y
        This allows you to add new versions to the tree in constant time
            Formally, is version V an ancestor of version W
                True iff bv < bw < ew < ev
                    This means the first visit to v happens before visiting w
                    the last visit to v happens after the last visit to w
    Any pointer-machine data structure can be made fully persistent with O(1) amortized factor overhead
    In order to store mods, you need 2 * (number of fields or in degree) + (number of pointers or out degree) + 1)
    To modify ie node.field = x
        if node not full: add mod
        else...
            split the node into two halves each half full of mods
            The old node is where it used to be
            Make a new node
            Apply half of the mods from the old node to the new node
                This is actually splitting a tree of mods such that half the nodes are in a new tree
                This will be (d + p + 1) mods
            recursively update at most 2d + 2p + 1 pointers to the node
        Potential function
            -c * sum(# of empty mod slots)
            Subtract recursion as c * 2 * (d + p + 1)
    Deamortized costs
        O(1) worst case in partial persistence modification
        Open problem in full persistence modification
Confluent persistence
    Consider a string. Every time you split the string, you have one more string
        Every time you concatenate, you have 1 less string
        If you pick random spots to copy and paste, you can double the size of the string in O(1)
            in x updates, you could get a size of 2 ^ x
    effective depth of a version ie e(v):
        1 + log($ of paths from root to vertex)
        overhead:
            log(# of updates) + max(effective depth)
        Lower bound:
            sum(e(v))
disjoint transform
    if you assume that confluent operations are performed only on two versions with no shared nodes
    Then you can get O(log(n)) overhead
functional data structures
    Balanced binary search trees, search and mod takes O(log(n))
    dequeues with concatenation in O(1)
    log(n) separation from functional to optimal
'''