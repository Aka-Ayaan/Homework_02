from HashTable import *

def create_studentDatabase(studentRecords):
    
    size = 7
    H = create_hashtable(size)

    for r in studentRecords:

        H, size = put(H, r['ID'], r, size)
    
    return H
    
def perform_Operations(H, operationFile):
    
    size = len(H[0])
    operations = []
    collision_path = {}
    
    with open(operationFile) as file:
        lines = file.readlines()
        
    for line in lines:
        operations.append(line.strip())

    # print(operations)

    count = 1
    for op in operations:

        Todo = op.split(' ')
        # print(Todo[0])
        if Todo[0].upper() == 'FIND':
            key = Todo[1]
            collision_path = get(H, key, size, collision_path, count)

        elif Todo[0].upper() == 'UPDATE':
            key = Todo[1]
            columnName = Todo[2]
            data = Todo[3]
            Update(H, key, columnName, data, size, collision_path, count)

        elif Todo[0].upper() == 'DELETE':
            key = Todo[1]
            H, size = delete(H, key, size, collision_path, count)

        count += 1    
            
    return collision_path

def main(filename):
   
    studentRecords=[] # List of dictionaries where each dictionary represents a student record
    StR = [] # List of lists where each list represents a student record

    with open(filename) as file:
        for line in file:
            StR.append(line.strip().split(','))

    for i in range(1,len(StR)):
        studentRecords.append({'SNo': StR[i][0],'ID': StR[i][1],'FirstName': StR[i][2],'LastName': StR[i][3], 'Sex': StR[i][4], 'Email': StR[i][5], 'Phone': StR[i][6], 'Department': StR[i][7]})

    return studentRecords
    

studentRecords=main('data.csv')
# print(studentRecords)
H=create_studentDatabase(studentRecords)
# print(H)
H = (['1bA7A3dc874da3c', None, '8e4FB470FE19bF0', None, None, 'bE9EEf34cB72AF7', '2EFC6A4e77FaEaC', 'baDcC4DeefD8dEB', None, 'DbeAb8CcdfeFC2c', None, None, 'bfDD7CDEF5D865B', 'f90cD3E76f1A9b9', 'A31Bee3c201ef58', '88F7B33d2bcf9f5', None], [{'SNo': '5', 'ID': '1bA7A3dc874da3c', 'FirstName': 'Lori', 'LastName': 'Todd', 'Sex': 'Male', 'Email': 'buchananmanuel@example.net', 'Phone': '689-207-3558x7233', 'Department': 'CE'}, None, {'SNo': '10', 'ID': '8e4FB470FE19bF0', 'FirstName': 'Isaiah', 'LastName': 'Downs', 'Sex': 'Male', 'Email': 'virginiaterrell@example.org', 'Phone': '+1-511-372-1544', 'Department': 'CS'}, None, None, {'SNo': '7', 'ID': 'bE9EEf34cB72AF7', 'FirstName': 'Katherine', 'LastName': 'Buck', 'Sex': 'Female', 'Email': 'conniecowan@example.com', 'Phone': '+1-773-151-6685', 'Department': 'CE'}, {'SNo': '8', 'ID': '2EFC6A4e77FaEaC', 'FirstName': 'Ricardo', 'LastName': 'Hinton', 'Sex': 'Male', 'Email': 'wyattbishop@example.com', 'Phone': '001-447-699-7998', 'Department': 'EE'}, {'SNo': '9', 'ID': 'baDcC4DeefD8dEB', 'FirstName': 'Dave', 'LastName': 'Farrell', 'Sex': 'Male', 'Email': 'nmccann@example.net', 'Phone': '603-428-2429x27392', 'Department': 'CS'}, None, {'SNo': '3', 'ID': 'DbeAb8CcdfeFC2c', 'FirstName': 'Kristine', 'LastName': 'Travis', 'Sex': 'Male', 'Email': 'bthompson@example.com', 'Phone': '277.609.7938', 'Department': 'EE'}, None, None, {'SNo': '6', 'ID': 'bfDD7CDEF5D865B', 'FirstName': 'Erin', 'LastName': 'Day', 'Sex': 'Male', 'Email': 'tconner@example.org', 'Phone': '001-171-649-9856x5553', 'Department': 'CS'}, {'SNo': '2', 'ID': 'f90cD3E76f1A9b9', 'FirstName': 'Phillip', 'LastName': 'Summers', 'Sex': 'Female', 'Email': 'bethany14@example.com', 'Phone': '214.112.6044', 'Department': 'CS'}, {'SNo': '4', 'ID': 'A31Bee3c201ef58', 'FirstName': 'Yesenia', 'LastName': 'Martinez', 'Sex': 'Male', 'Email': 'kaitlinkaiser@example.com', 'Phone': '584.094.6111', 'Department': 'EE'}, {'SNo': '1', 'ID': '88F7B33d2bcf9f5', 'FirstName': 'Shelby', 'LastName': 'Terrell', 'Sex': 'Male', 'Email': 'elijah57@example.net', 'Phone': '001-084-906-7849', 'Department': 'CS'}, None])
print(perform_Operations(H, 'operations.txt'))