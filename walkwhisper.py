import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--func", type=str, required=True, help="A single and/or comma delimited list of Windows API functions to look up")
parser.add_argument("--header", type=str, default="/usr/x86_64-w64-mingw32/include/wincrypt.h,/usr/x86_64-w64-mingw32/include/synchapi.h,/usr/x86_64-w64-mingw32/include/processthreadsapi.h,/usr/x86_64-w64-mingw32/include/tlhelp32.h,/usr/x86_64-w64-mingw32/include/winnt.h,/usr/x86_64-w64-mingw32/include/memoryapi.h,/usr/x86_64-w64-mingw32/include/winuser.h", required=False, help="A single or comma delimited list of the Windows header file(s) that need to be parsed")
parser.add_argument("--def", action='store_true', required=False, help="Prints the WinAPI Definition")
dict = vars(parser.parse_args())

if "func" in dict.keys():
    dict["func"] = [s.strip() for s in dict["func"].split(",")]
if "header" in dict.keys():
    dict["header"] = [s.strip() for s in dict["header"].split(",")]

def customAPIHash(line, funct):
     final = line.split(" ")
     newfinal = ""
     splitFunct = {"",""}
     for index,w in enumerate(final):
         if funct in w:
             splitFunct = w.split("(")
             if splitFunct[0] == funct:
                 if dict['def'] == True:
                     print(line)
                 if len(splitFunct) > 1: 
                     newfinal = splitFunct[0] + " = HANDLE(NTAPI*)(" + splitFunct[1]
                 else:
                     newfinal = splitFunct[0] + " = HANDLE(NTAPI*)("
                     final[index+1] = final[index+1].replace("(","")
         else:
             newfinal = newfinal + " " + w + " "
     if splitFunct[0] == funct:
         print("using custom" + newfinal)

def hash_djb2(s):
    hash = 5381
    for x in s:
        hash = (( hash << 5) + hash) + ord(x)
    return hash & 0xFFFFFFFF

def usingAPI(line, funct):
     final = line.split(" ")
     newfinal = ""
     hash = ""
     splitFunct = {"",""}
     for index,w in enumerate(final):
          if funct in w:
              splitFunct = w.split("(")
              if splitFunct[0] == funct:
                  hash = hex(hash_djb2(splitFunct[0]))
                  if len(splitFunct) > 1:
                      newfinal = newfinal + splitFunct[0] + " " + splitFunct[0] + " = (custom" + splitFunct[0] + ")getFunctionAddressByHash((char*)\"DLL NAME HERE\"," + hash + ");"
                  else:
                      newfinal = splitFunct[0] + " "+ splitFunct[0]  +" = (custom" + splitFunct[0] + ")getFunctionAddressByHash((char*)\"DLL NAME HERE\"," + hash + ");"

     if splitFunct[0] == funct:
          print("custom" + newfinal + "\n")


print("""
 _    _  ___   _      _   ___    _ _   _ _____ ___________ ___________ 
| |  | |/ _ \ | |    | | / / |  | | | | |_   _/  ___| ___ \  ___| ___ \ 
| |  | / /_\ \| |    | |/ /| |  | | |_| | | | \ `--.| |_/ / |__ | |_/ / 
| |/\| |  _  || |    |    \| |/\| |  _  | | |  `--. \  __/|  __||    / 
\  /\  / | | || |____| |\  \  /\  / | | |_| |_/\__/ / |   | |___| |\ \ 
 \/  \/\_| |_/\_____/\_| \_/\/  \/\_| |_/\___/\____/\_|   \____/\_| \_| 

""")
print("NO UNDOCUMENTED WINDOWS API WILL BE OUTPUT PLEASE REFER TO http://undocumented.ntinternals.net/ \n")

for f in dict["header"]:
     with open(f, 'r') as f:
          for line in f.readlines():
               if 'WINAPI' in line:
                    line = line.lstrip()
                    if not (line.startswith('#', 0)):
                        line = line.rstrip()
                        line = line.replace('WINBASEAPI ', '')
                        line = line.replace('WINUSERAPI ', '')
                        line = line.replace('WINAPI ', '')
                        line = line.replace('WINBOOL ', 'BOOL ')
                        if dict["func"] == "":
                            print("NO FUNCTION PROVIDED")
                        else:
                            for f in dict["func"]:
                                if f in line:
                                    customAPIHash(line, f)
                                    usingAPI(line, f)
