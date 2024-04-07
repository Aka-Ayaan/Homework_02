import math

def create_hashtable(size): # returns tuple(list,list)
    
    return ([None] * size, [None] * size)   # Initializing hashtable

def isPrime(n): # For checking prime number
     
    # Corner cases 
    if(n <= 1):
        return False
    if(n <= 3):
        return True
     
    # This is checked so that we can skip middle five numbers in the loop below
    if(n % 2 == 0 or n % 3 == 0):
        return False
     
    for i in range(5,int(math.sqrt(n) + 1), 6): 
        if(n % i == 0 or n % (i + 2) == 0):
            return False
     
    return True

def repopulate_table(newtable, oldtable, size): # helper function for resize_hashtable

    for i in range(len(oldtable[0])):
        if oldtable[0][i] != None:
            key = oldtable[0][i]
            data = oldtable[1][i]
            newtable,size = put(newtable, key, data, size)

    return newtable, size            

def resize_hashtable(hashtable, size, increase): #return hashtable,size

    # For increasing the size of the hashtable
    if increase:
        size = size * 2
        while not isPrime(size):
            size += 1

    # For decreasing the size of the hashtable
    elif not increase and size // 2 >= 7:
        size = size // 2
        while not isPrime(size):
            size += 1

    # No need to resize if condition false
    else:
        return hashtable, size

    newtable = create_hashtable(size)

    # Popualting the new hashtable with the old values and return
    return repopulate_table(newtable, hashtable, size)

def hash_function(key, size): #returns integer (Address)
    
    total = 0

    for i in key:
        total += ord(i)

    total = total >> 4

    return total % size

def collision_resolver(key, oldAddress, size): #returns integer (Address)
    
    total = 0

    for i in key:
        total += ord(i)

    total = total // size

    return (total + oldAddress) % size

def put(hashtable, key, data, size): #return hashtable,size
    
    newhash = 0
    hashvalue = hash_function(key,size)
    
    if hashtable[0][hashvalue] == None:   # If key none then update both key and Data
        hashtable[0][hashvalue] = key
        hashtable[1][hashvalue] = data
    
    else:      # If key none then update both key and Data
        if hashtable[0][hashvalue] == key:
            hashtable[1][hashvalue] = data
    
        else:   # Resolving collisions
            newhash = collision_resolver(key,hashvalue,size)
            while hashtable[0][newhash] != None and hashtable[0][newhash] != key and hashtable[0][newhash] != '#':
                newhash = collision_resolver(key, newhash, size)
    
            if hashtable[0][newhash] == None:   # If key none then update both key and Data
                hashtable[0][newhash] = key
                hashtable[1][newhash] = data
    
            else:     # If key none then update both key and Data
                if hashtable[0][newhash] == key:
                    hashtable[1][newhash] = data

    # Resizing the hashtable
    if loadFactor(hashtable,size) > 0.75:
        hashtable,size = resize_hashtable(hashtable,size,True)

    return hashtable, size

def loadFactor(hashtable, size): # returns a float - Loadfactor of hashtable
    
    count = 0
    
    for i in hashtable[0]:
        if i is not None and i != '#':   # Checks for the number of filled slots (tombstones not counted)
            count += 1

    return count / size

def Update(hashtable, key, columnName, data, size, collision_path, opNumber): # returns Nothing, prints 'record Updated'
    
    start = hash_function(key,size)
    pos = start
    collision_path[opNumber] = []   # Initializing the collision path

    while hashtable[0][pos] != None and hashtable[0][pos] != '#':
        
        if hashtable[0][pos] == key:
            hashtable[1][pos][columnName] = data
            collision_path[opNumber].append(pos)   # Updating the collision path
            print('record Updated')
            break
    
        else:
            collision_path[opNumber].append(pos)   # Updating the collision path in case of coliision
            pos = collision_resolver(key, pos, size)
            if pos == start:
                print('Item not found')
                break
                
def get(hashtable,key,size,collision_path,opNumber): # returns dictionary

    start = hash_function(key,size)
    pos = start
    collision_path[opNumber] = []   # Initializing the collision path

    while hashtable[0][pos] != None:
            
        if hashtable[0][pos] == key:
            collision_path[opNumber].append(pos)   # Updating the collision path
            return hashtable[1][pos]
            
        else:
            collision_path[opNumber].append(pos)   # Updating the collision path in case of collision
            pos = collision_resolver(key, pos, size)
            if pos == start:
                print('Item Not Found')
                break   
        
def delete(hashtable, key, size,collision_path,opNumber): #returns hashtable, size, prints a msg  'Item Deleted'
    
    newhash = 0
    hashvalue = hash_function(key,size)
    collision_path[opNumber] = []   # Initializing the collision path

    collision_path[opNumber].append(hashvalue)   # Updating the collision path

    if hashtable[0][hashvalue] != key:
        newhash = collision_resolver(key, hashvalue, size)
        collision_path[opNumber].append(newhash)
        
        while hashtable[0][newhash] != key:
            newhash = collision_resolver(key, newhash,size)
            collision_path[opNumber].append(newhash)   # Updating the collision path in case of collision
            
        # Adding tombstones to the deleted item if while loop runs
        if hashtable[0][newhash] == key:
            hashtable[0][newhash] = "#"
            hashtable[1][newhash] = "#"
            print('Item Deleted')
    
    # Adding tombstones to the deleted item if while loop doesn't run
    else:
        hashtable[0][hashvalue] = "#"
        hashtable[1][hashvalue] = "#"
        print('Item Deleted')

    # Resizing the hashtable
    if loadFactor(hashtable,size) < 0.30:
        hashtable,size = resize_hashtable(hashtable,size,False)

    return hashtable, size    
