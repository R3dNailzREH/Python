"""
Name: check_duplicates
Version: 0.1
Date: 24Oct20

Description:
Run in a directory of downloaded files. The script will open a file with a
list of all the files that were previously downloaded. It will check all the
files in the current folder against that list. If the file already exists the
new file is a duplicate. It will be moved to a file called ./duplicates
If it is not in the list it will be added. The updated file will be saved in
the same folder.

Once the script has been run, all the files still in the folder are new and
can be saved into the archive.

This way I can keep putting downloaded files where I want them instead of
keeping them in a separate area forever.

Maintains a list of files that have already been downloaded in a file
called history.log.

LIMITATIONS:
* It must exist the folder where the script is run

FUTURE:
*  Specify the log file
"""

# The log file contains all the files downloaded from a location
# format:
import csv
import os
import shutil
import sys

# TODO: Make this a command line parameter
lsLogFileName = "youtube.log"
lsBackupFileName = lsLogFileName + '.bak'
lnNewFiles = 0
lnDupFiles = 0

# open the file with a list of everything we downloaded already
lcLogFileHandle = open(lsLogFileName, 'r')
lcAlreadyDownloadedFileDictionary = {}

# read the contents into a dictionary
for lsCurrentReadLine in lcLogFileHandle:
    laCurrentLineSplit = lsCurrentReadLine.strip().split(',')  # split around the = sign
    print("key: ", laCurrentLineSplit[0], " value: ", laCurrentLineSplit[1])
    if len(laCurrentLineSplit) > 1:  # we have the = sign in there
        lcAlreadyDownloadedFileDictionary[laCurrentLineSplit[0]] = laCurrentLineSplit[1]

# get a list of files in the current folder
# TODO: Make this a command line parm
lsFolderName = "."
laListOfFiles = os.listdir(lsFolderName)

# If filename is in the dictionary move it to the duplicates folder
# If it's not in the list, add it to the list
for lsFileEntry in laListOfFiles:
    sys.stdout.write("\nCurrent file: ")
    sys.stdout.write(lsFileEntry)
    # Don't index our log files or subdirectories
    if (lsFileEntry == lsBackupFileName or lsFileEntry == lsLogFileName
            or lsFileEntry == "check_duplicates.py"):
        continue
    if (os.path.isdir(lsFileEntry)):
        continue
    if lsFileEntry in lcAlreadyDownloadedFileDictionary.keys():
        lnDupFiles = lnDupFiles + 1
        sys.stdout.write(" is Duplicate")
        lsDupFolderName = "duplicates"
        if not os.path.isdir(lsDupFolderName):
            os.mkdir(lsDupFolderName)
        shutil.move(lsFileEntry, lsDupFolderName)
    else:
        lnNewFiles = lnNewFiles + 1
        sys.stdout.write(" NEW  ")
        # TODO: Add the file size to the check just in case
        print("key: ", lsFileEntry, " value: ", 1)
        lcAlreadyDownloadedFileDictionary[lsFileEntry] = "1"

# Save dictionary back out to file
# Create backup
if os.path.isfile(lsBackupFileName):
    os.remove(lsBackupFileName)

shutil.copyfile(lsLogFileName, lsBackupFileName)

# write current dictionary
with open(lsLogFileName, 'w') as lcNewLogFileHandle:
    # print(lcAlreadyDownloadedFileDictionary, file=lcNewLogFileHandle)
    for lsKey in lcAlreadyDownloadedFileDictionary.keys():
        lsTempString = lsKey + ',' + lcAlreadyDownloadedFileDictionary[lsKey]
        print(lsTempString, file=lcNewLogFileHandle)

# Print stats
print("\nSUMMARY:")
print("NEW: ", lnNewFiles)
print("Dup: ", lnDupFiles)
print("TOTAL: ", lnNewFiles + lnDupFiles)
# done
