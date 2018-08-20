############################################################
#CreateDynDictionary

# Description: Create a Dictionary that loads the contents of
# xl-deploy branch of a repository. Link that dictionary to the 
# environment object. Load values from file.

#Assumptions:
# The following parameters will be passed in:
#	1. Application Name (This must be the name of the application in XL-Deploy
#   2. Technology (ie JBOSS, WAS85)
#   3. FileName to use for dictionary values (must be in the form of env.properties)
#
#   
# The dictionary is only created if it doesn't already exist but the non encrypted 
# values are always replaced.

import sys
import os
import re

#Get passed in arguments
if len(sys.argv)!= 4:
    print ("Script requires 3 parameters")
    exit()
AppName=sys.argv[1]
Technology=sys.argv[2]
FileName=sys.argv[3]
IsDefaultFile=False

#AppName="BREWASDeployTestDev"
#Technology="WAS85"
#FileName="ACC.properties"

#Parse FileName to get ENV and determine if this is a default properties file
FileParts=FileName.split(".")
if len(FileParts) == 2:
    Env=FileParts[0].upper()
elif len(FileParts) == 3:
    Env=FileParts[0].upper()
    Technology=FileParts[1]
    IsDefaultFile = True
else:
    print FileName + " is not a valid file name\n"
    exit()

#Create Dictionary & associate with environment
EnvPath="Environments/" + Env + "/" + Technology
DictPath="Environments/" + Env + "/Dictionaries/" + Technology + "/" + AppName + "_Dictionary"
if not (repository.exists(DictPath)):
    dict=factory.configurationItem(DictPath,"udm.Dictionary")
    if not IsDefaultFile:
        Restricts=[]
        Restricts.append("Applications/" + AppName)
        dict.restrictToApplications=Restricts
    print "About to create dictionary"
    repository.create(dict)
    print ("created " + dict.id\t)
    #Add new dictionary to Environment Object in XL-D
    if repository.exists(EnvPath):
        ENVObject = repository.read(EnvPath)
        CurrentDictionaries=ENVObject.dictionaries
        #Since default dictionaries for a technology must be at the end of the list,
        #need to make sure the new entry is always added to the top if it is not a
        #default dictionary and to the bottom if it is a default dictionary
        dict=repository.read(DictPath)
        dictList=[dict.id]
        if IsDefaultFile:
            dictionaries=CurrentDictionaries + dictList
        else:
            dictionaries=dictList + CurrentDictionaries
        print ("setting dictionaries on " + ENVObject.id + " to \n")
        print dictionaries\n
        ENVObject.dictionaries=dictionaries
        repository.update(ENVObject)
    else:
        print EnvPath + " does not exist"

#Load key / value pairs from file into non encrypted vales list in dictionary
ScriptDir=os.path.dirname(sys.argv[0])
FilePath=os.path.join(ScriptDir, FileName)
pattern = re.compile(r"\s*=\s*|\s*:\s*")
PropFile = open(FilePath,"r")
KeyValueList = {}
SplitLine=[]
for line in PropFile.readlines():
        SplitLine=re.split(pattern,line,1,0)
        if (len(SplitLine) == 2) and (SplitLine[0][0] != "#"):
            KeyValueList[SplitLine[0].strip()] = SplitLine[1].strip()
            print "KVP: " + SplitLine[0].strip() + "," + SplitLine[1].strip()
        else:
            print "The following line was not parsed:"
            print line
dict=repository.read(DictPath)
dict.entries=KeyValueList
repository.update(dict)


