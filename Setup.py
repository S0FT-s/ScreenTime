import os 
from sys import  executable

user = os.getlogin()
path = os.getcwd()
RunPATH = fr"C:\Users\{user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

#Prepare the code to go inside a vbs file
RunPart = f'WshShell.Run """{executable}""'

#Creates the .bat file
with open("ScreenTime_DB.vbs","w") as f:
    f.write(f'Set WshShell = CreateObject("WScript.Shell")\n{RunPart} ""{path}\\main.pyw""", 0')
    f.close()

with open("Screentime_Background_Site.vbs","w") as r:
    r.write(f'Set WshShell = CreateObject("WScript.Shell")\n{RunPart} ""{path}\\site\\backend\\server.pyw""", 0')
    r.close()

print("[+] VBS code created.")
print("[!] To run on startup, place it inside the Startup folder.")
print(f"{RunPATH}")
