from time import localtime, sleep
import sqlite3
import os.path


#A fazer meter o program para atualizar a meia noite

base_dir = os.path.dirname(__file__)
pathDB = os.path.join(base_dir, "DataBase","TimeStorage.db")

def DataBaseCreation():
    #this line of code only runs if it is the firts time running the program
    #it just create the DB
    print("[+] Creating the Database")
    con = sqlite3.connect(pathDB)
    cur = con.cursor()
    res = cur.execute("CREATE TABLE time(month INTEGER, day INTEGER, time INTEGER)")
    res.fetchall()
    con.close()

"""""
To write to the database the time needs to be in minutes
MODES 
w = WRITE
U = UPDATE
"""
#DataBase Write and edit
def DataBaseWE(mode, month, day, min):
    con = sqlite3.connect(pathDB)
    cur = con.cursor()
    data = [month,day, min]

    if mode == "w":
        data = [month,day, min]
        dataCheck = [month, day]

        cur.execute("SELECT count(*) FROM time WHERE month = ? AND day = ?",dataCheck)
        returnValue = cur.fetchone()[0] #range between 0-1 (0 = not exist) and (1 = exist)
        #print (returnValue)
        if returnValue == 0:
            print("[+] Value does not exist, writing new data.")
            cur.execute("INSERT INTO time VALUES(?, ?, ?)",data)
            con.commit()
        else: 
            print("[-] Row already exist")
        #Check  to avoid duplicates
               
    if mode == "u":
        datatesy = [month,day]  
        #TO GET THE DATA
        current_min = cur.execute("SELECT time FROM time WHERE month = ? AND day = ?",datatesy)
        current_minINT = current_min.fetchone()[0]
        print(current_minINT)
        
        data = [current_minINT+min,month, day] 
        cur.execute("UPDATE time SET time = ? WHERE month = ? AND day = ?",data)
        con.commit()
        current_min = cur.execute("SELECT time FROM time WHERE month = ? AND day = ?",datatesy)
        valor = current_min.fetchone()[0]
        print("min atual na db",valor)
        con.close()

# Deletes database records from 4 or more months ago
def deleteOldRecords():
    # Number of months to go back for deletion
    DeletingValue = 4
    month = (localtime().tm_mon - DeletingValue - 1) % 12 + 1#
    con = sqlite3.connect(pathDB)
    cur = con.cursor()
    cur.execute("DELETE FROM time WHERE month = ?", (month,))
    con.commit()
    con.close()


#This function just run once one the starup
def StartUp():
    day = localtime().tm_mday
    month = localtime().tm_mon
    DataBaseWE("w",month,day,0)
    return day ,month

def main():
# Checks if the folder and database exist; if not, creates them.
    if os.path.isdir(pathDB) == False:
        os.mkdir(base_dir+"/DataBase")
        DataBaseCreation()
    else:
        print("[*] Database already created")
        deleteOldRecords()

    #only runs one time and creates a row
    day, month = StartUp()

    minys = 0
#with this loop is add 2 more minus to the screen time of that day
    try:
        print("Starting loop")
        while True:
            sleep(60)
            DataBaseWE("u",month,day,1)
            minys += 1
            if day != localtime().tm_mday:
                day, month = StartUp()
    except KeyboardInterrupt:
        print("user leave")
        print(minys)

main()