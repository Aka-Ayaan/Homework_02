from HashTable import *

def create_studentDatabase(studentRecords):
    
    size = 7
    H = create_hashtable(size)

    for r in studentRecords:

        H, size = put(H, r['ID'], r, size)
    
    return H
    
# def perform_Operations(operationFile):
    
#     H = create_studentDatabase(studentRecords)
#     size = 7
    
#     with open(operationFile) as file:
#         operations = file.readlines()
#         # print(operations)

#         for op in operations:
#             op = op.strip()
#             op = op.split(' ')
#             # print(op)

#             if op[0] == 'Find':
#                 data = get(H,op[1],size)
#                 if op[2] = 
                  

        



            

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
print(H)
# print(perform_Operations('Operations.txt'))