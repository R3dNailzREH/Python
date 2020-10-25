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
* Script must exist the folder where the script is run
* Only checks filename for dup, doesn't compare file size
* If the file is already in /duplicates the script will fail if it tries to
  to move another file with the same name into the /duplicates folder

FUTURE:
* Add support for file size
* Add support for duplication in the /duplicates folder
"""

# The log file contains all the files downloaded from a location
# format:
import os
import shutil
import sys

# If they don't give a logfile name, tell them it's required and exit
if len(sys.argv) < 2:
    print("Usage:\n  python check_duplicates LOGFILE_NAME")
    exit(1)

# If they give a name that doesn't exist, ask if they want to create it
# If they do, create an empty file with that name so we can let the open
# routine run and read no keys.
lsLogFileName = sys.argv[1]
if not os.path.isfile(lsLogFileName):
    print("File not found: ", lsLogFileName)
    lsKeypress = input("To create a new logfile, press y, or any other character to abort: ")
    if ("y" == lsKeypress or "Y" == lsKeypress):
        with open(lsLogFileName, 'w') as fp:
            pass
    else:
        exit(1)

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
lsFolderName = "."
laListOfFiles = os.listdir(lsFolderName)

# If filename is in the dictionary move it to the duplicates folder
# If it's not in the list, add it to the list

# TODO: It tracks the file size but I'll need a strat for dupkeys.
#       maybe just filename_size as the key and not use a dict?
for lsFileEntry in laListOfFiles:
    sys.stdout.write("\nCurrent file: ")
    sys.stdout.write(lsFileEntry)
    # Don't index our log files or subdirectories
    if (lsFileEntry == lsBackupFileName or lsFileEntry == lsLogFileName
            or lsFileEntry == "check_duplicates.py"):
        continue
    if (os.path.isdir(lsFileEntry)):
        sys.stdout.write(" is Folder")
        continue
    if lsFileEntry in lcAlreadyDownloadedFileDictionary.keys():
        lnDupFiles = lnDupFiles + 1
        sys.stdout.write(" is Duplicate --> Move to /duplicates")
        lsDupFolderName = "duplicates"
        if not os.path.isdir(lsDupFolderName):
            os.mkdir(lsDupFolderName)
        shutil.move(lsFileEntry, lsDupFolderName)
    else:
        lnNewFiles = lnNewFiles + 1
        sys.stdout.write(" NEW  ")
        # TODO: Add the file size to the check just in case
        lnFileSize = os.path.getsize(lsFileEntry)
        print("key: ", lsFileEntry, " value: ", lnFileSize)
        lcAlreadyDownloadedFileDictionary[lsFileEntry] = lnFileSize

# Save dictionary back out to file
# Create backup
if os.path.isfile(lsBackupFileName):
    os.remove(lsBackupFileName)

shutil.copyfile(lsLogFileName, lsBackupFileName)

# write current dictionary
with open(lsLogFileName, 'w') as lcNewLogFileHandle:
    # print(lcAlreadyDownloadedFileDictionary, file=lcNewLogFileHandle)
    for lsKey in lcAlreadyDownloadedFileDictionary.keys():
        lsTempString = lsKey + ',' + str(lcAlreadyDownloadedFileDictionary[lsKey])
        print(lsTempString, file=lcNewLogFileHandle)

# Print stats
print("\nSUMMARY:")
print("NEW: ", lnNewFiles)
print("Dup: ", lnDupFiles)
print("TOTAL: ", lnNewFiles + lnDupFiles)
# done
