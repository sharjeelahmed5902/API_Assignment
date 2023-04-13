from jproperties import Properties
propfile = Properties()
import os

# Get the current working directory
current_directory = os.getcwd()
print("current_directory",current_directory)

# Set the directory path where the "Config.properties" file is located
directory_path = os.getcwd()+ '\\TestCases\\Config.properties'
print("directory_path",directory_path)
class PropReader:
   def readProp(Key):
       with open(directory_path, "rb") as configfile:
        propfile.load(configfile)
        return propfile.get(Key).data

#
# P = PropReader
# print(P.readProp("url"))