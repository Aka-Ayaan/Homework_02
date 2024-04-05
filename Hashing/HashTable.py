# import sympy
import math

def create_hashtable(size): # returns tuple(list,list)
    
    return ([None] * size, [None] * size)


def isPrime(n):
     
    # Corner cases 
    if(n <= 1):
        return False
    if(n <= 3):
        return True
     
    # This is checked so that we can skip 
    # middle five numbers in below loop 
    if(n % 2 == 0 or n % 3 == 0):
        return False
     
    for i in range(5,int(math.sqrt(n) + 1), 6): 
        if(n % i == 0 or n % (i + 2) == 0):
            return False
     
    return True

def resize_hashtable(hashtable,size,increase): #return hashtable,size

    if increase:
        size = size * 2
        while not isPrime(size):
            size += 1

    elif not increase and size // 2 >= 7:
        size = size // 2
        while not isPrime(size):
            size += 1

    else:
        return hashtable, size

    newtable = create_hashtable(size)

    for i in range(len(hashtable[0])):

        if hashtable[0][i] != None:
            key = hashtable[0][i]
            data = hashtable[1][i]
            hashvalue = hash_function(key, size)

            if newtable[0][hashvalue] == None:
                newtable[0][hashvalue] = key
                newtable[1][hashvalue] = data
            else:
                if newtable[0][hashvalue] == key:
                    newtable[1][hashvalue] = data
                else:
                    newhash = collision_resolver(key,hashvalue,size)
                    while newtable[0][newhash] != None and newtable[0][newhash] != key and hashtable[0][newhash] != '#':
                        newhash = collision_resolver(key,newhash,size)
                    if newtable[0][newhash] == None:
                        newtable[0][newhash] = key
                        newtable[1][newhash] = data
                    else:
                        if newtable[0][newhash] == key:
                            newtable[1][newhash] = data

        
    return newtable,size

def hash_function(key,size): #returns integer (Address)
    
    total = 0

    for i in key:
        total += ord(i)

    total = total >> 4

    return total % size

def collision_resolver(key,oldAddress,size): #returns integer (Address)
    
    total = 0

    for i in key:
        total += ord(i)

    total = total // size
    address = ((total + oldAddress) % size)

    return address

def put(hashtable,key, data,size): #return hashtable,size
    
    newhash = 0

    hashvalue = hash_function(key,size)
    if hashtable[0][hashvalue] == None:
        hashtable[0][hashvalue] = key
        hashtable[1][hashvalue] = data
    else:
        if hashtable[0][hashvalue] == key:
            hashtable[1][hashvalue] = data
        else:
            newhash = collision_resolver(key,hashvalue,size)
            while hashtable[0][newhash] != None and hashtable[0][newhash] != key and hashtable[0][newhash] != '#':
                newhash = collision_resolver(key, newhash, size)
            if hashtable[0][newhash] == None:
                hashtable[0][newhash] = key
                hashtable[1][newhash] = data
            else:
                if hashtable[0][newhash] == key:
                    hashtable[1][newhash] = data

    if loadFactor(hashtable,size) > 0.75:
        hashtable,size = resize_hashtable(hashtable,size,True)

    return hashtable, size

def loadFactor(hashtable,size): # returns a float - Loadfactor of hashtable
    
    count = 0
    
    for i in hashtable[0]:
        if i is not None:
            count += 1

    return count / size

def Update(hashtable,key, columnName, data,size,collision_path,opNumber): # returns Nothing, prints 'record Updated'
    pass
        
def get(hashtable,key,size,collision_path,opNumber): # returns dictionary
    
    count = 1
    start = hash_function(key,size)
    pos = start
    
    while hashtable[0][pos] != None:
        if hashtable[0][pos] == key:
            return hashtable[1][pos]
        else:
            pos = collision_resolver(start,size,count)
            collision_path[start].append(pos)
            count += 1
            if pos == start:
                return 'Item not found'
            
    print(collision_path)


        
def delete(hashtable, key, size,collision_path,opNumber): #returns hashtable, size, prints a msg  'Item Deleted'
    
    newhash = 0
    count = 0
    hashvalue = hash_function(key,size)
    
    if hashtable[0][hashvalue] != key:
        newhash = collision_resolver(key, hashvalue, size)
        while hashtable[0][newhash] != key and count != size:
            newhash = collision_resolver(key, newhash,size,)
            collision_path[hashvalue].append(newhash)
        if hashtable[0][newhash] == key:
            hashtable[0][newhash] = "#"
            hashtable[1][newhash] = "#"
    else:
        hashtable[0][hashvalue] = "#"
        hashtable[1][hashvalue] = "#"
