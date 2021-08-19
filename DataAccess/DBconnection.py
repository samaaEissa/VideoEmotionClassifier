import pyodbc 

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-HTQ1DNE;'
                      'Database=Emotion_Analysis;'
                      'Trusted_Connection=yes;')                      

# cursor = conn.cursor()
# cursor.execute('SELECT * FROM Customer;')

#for row in cursor:
#    print(row)
    
    



def Registeration(U_Name,U_Password,U_Email):
   
    cursor = conn.cursor() 
    query="insert into Customer(U_Name,U_Password,U_Email) values (?, ?,?)"
    values=(U_Name,U_Password ,U_Email)
    cursor.execute(query,values)
    conn.commit()   
    
#----------------------------------------------------------------------------------    
def login(U_Email,U_Password):
    
    cursor = conn.cursor() 
    query="SELECT * FROM Customer where U_Email=? and U_Password=?  "
    values=(U_Email,U_Password)
    cursor.execute(query,values)
    conn.commit()   
    
    
    
#-------------------------------------------------------------------------------------