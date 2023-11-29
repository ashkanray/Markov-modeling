from collections.abc import MutableMapping
from functools import reduce
import time


class Hashtable(MutableMapping):
    # polynomial constant, used for _hash
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        self.capacity = capacity
        self._items = [None] * capacity
        self.default_value = default_value
        self.load_factor = load_factor
        self.growth_factor = growth_factor
        self.occupied = 0


    def _hash(self, key):
        """This method takes in a string and returns an integer value between 0 and self.capacity.
        This particular hash function uses Horner's rule to compute a large polynomial.
        See https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect10-hash-basics.pdf
        """

        val = 0
        for letter in key:
            val = self.P_CONSTANT * val + ord(letter)
        return val % self.capacity


    def __setitem__(self, key, val):
        ind = self._hash(key)

        if self._items[ind] is not None:

            #Checks if there's already a key existing in the hash table
            #If so, you overwrite the value

            dup_ind = 0
            dup_flag = False
            for tup in self._items[ind]:
                if tup[0] == key and tup[2] == True:
                    self._items[ind][dup_ind] = (key, val, True)
                    dup_flag = True
                    break
                dup_ind+=1

            if not dup_flag:
                self._items[ind].append((key, val, True))
            
        
        else:
            self._items[ind] = []
            self._items[ind].append((key, val, True))
            self.occupied += 1

        
        if (self.occupied / self.capacity) > self.load_factor:
            ####TIMER
            start = time.perf_counter()
            self.__rehash__()
            elapsed = time.perf_counter() - start
    


    def __getitem__(self, key):
        ind = self._hash(key)

        if self._items[ind] is None:
            return self.default_value

        else:
            for tup in self._items[ind]:
                if tup[0] == key and tup[2] == True:
                    return tup[1]
    
            return self.default_value



    def __delitem__(self, key):
        ind = self._hash(key)

        if self._items[ind] is None:
            raise KeyError


        if len(self._items[ind]) == 1:
            if self._items[ind][0][2] == False:
                raise KeyError

            else: 
                self._items[ind][0] = list(self._items[ind][0])
                self._items[ind][0][2] = False
                self._items[ind][0] = tuple(self._items[ind][0])
        
        else:
            index = 0
            for tup in self._items[ind]:
                if tup[0] == key and tup[2] == True:
                    temp = list(tup)
                    temp[2] = False
                    self._items[ind][index] = tuple(temp)
                    break
                index+=1
            
            if index == len(self._items[ind]):
                raise KeyError


    def __rehash__(self):
        self.occupied = 0
        self.capacity = self.capacity * self.growth_factor
        old_tab = self._items
        self._items = [None] * self.capacity

        for i in range(len(old_tab)):
            if old_tab[i] is not None:
                for tup in old_tab[i]:
                    if tup[2] == True:
                        self.__setitem__(tup[0], tup[1])


    def __len__(self):
        length = 0
        
        for item in self._items:
            if item is not None:
                for tups in item:
                    if tups[2] == True:
                        length+= 1
        
        return length

    def __str__(self):
        return str(self._items)


    def __iter__(self):
        """
        You do not need to implement __iter__ for this assignment.
        This stub is needed to satisfy `MutableMapping` however.)

        Note, by not implementing __iter__ your implementation of Markov will
        not be able to use things that depend upon it,
        that shouldn't be a problem but you'll want to keep that in mind.
        """
        raise NotImplementedError("__iter__ not implemented")
