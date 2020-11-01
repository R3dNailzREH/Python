"""
Name: check_duplicates
Version: 1.0
Date: 31Oct20

Description:
Run in a directory of downloaded files. The script will create or open a log 
file with a list of all the files that were previously downloaded. It will 
check all the files in the current folder against that list. If the file 
exists in the list with the same filename and file size, the new file is a
duplicate. It will be moved to a file called ./duplicates 

If it is not in the list it will be added. The updated log file will be saved 
in the same folder.

Once the script has been run, all the files still in the original folder did
not appear in the log file of files downloaded before. This means they are
new and can be moved elsewhere and renamed. If you accidentally download it
again, this script will keep you from keeping the duplicate.

This way I can keep taking downloaded files and move them elsewhere and rename
them instead of keeping them in a separate area forever with names I don't want.

SIDE EFFECTS:
* Script maintains a list of files in the current folder that have already been
  downloaded in a logfile specified by the user.
* Upon running, a .bak version is created should you need to revert your log.
* All files that appear in the log AND have the same file size will be moved to
  /duplicates
* All files NOT in the log OR with different sizes will be moved to /new_files

LIMITATIONS:
* Script must exist the folder where the script is run
* If the file is already in /duplicates or /new_files the script will fail if it
  tries to to move another file with the same name into the /duplicates folder

FUTURE:
* Add support for duplication in the target folders
"""

# The log file contains all the files downloaded from a location
# format:
import io
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

# Create the target folders. /new for files not in log, /dups if they are
lsDupFolderName = "duplicates"
if not os.path.isdir(lsDupFolderName):
    os.mkdir(lsDupFolderName)
lsNewFolderName = "new_files"
if not os.path.isdir(lsNewFolderName):
    os.mkdir(lsNewFolderName)

# open the file with a list of everything we downloaded already
lcLogFileHandle = open(lsLogFileName, 'r')
lcAlreadyDownloadedFileDictionary = {}

# read the contents into a dictionary
for lsCurrentReadLine in lcLogFileHandle:
    laCurrentLineSplit = lsCurrentReadLine.strip().split(',')  # split on comma delimiter
    # Build a key of filename_filesize so we can account for the same name but different sizes
    # This will be undone before writing the file back out so the user won't even see it.
    lsTempKeyString = laCurrentLineSplit[0] + "?" + str(laCurrentLineSplit[1])
    print("key: ", lsTempKeyString, " value: ", laCurrentLineSplit[1])
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
    # Don't index our script, log files or subdirectories
    if (lsFileEntry == lsBackupFileName or lsFileEntry == lsLogFileName
            or lsFileEntry == "check_duplicates.py"):
        continue
    if ( os.path.isdir(lsFileEntry) ):
        sys.stdout.write(" is Folder")
        continue
    # We're going to process the file so get the size and build the composite key
    # We use a question mark for our separator because it's not legal in a filename
    # so it should never already exist in the filename we're using.
    lnFileSize = os.path.getsize(lsFileEntry)
    lsTempKeyString = lsFileEntry + "?" + str(lnFileSize)
    if lsTempKeyString in lcAlreadyDownloadedFileDictionary.keys():
        lnDupFiles = lnDupFiles + 1
        sys.stdout.write(" is Duplicate --> Move to /duplicates")
        shutil.move(lsFileEntry, lsDupFolderName)
    else:
        lnNewFiles = lnNewFiles + 1
        sys.stdout.write(" NEW --> Move to /new_files")
        shutil.move(lsFileEntry, lsNewFolderName)
        print("\n\t-->key: ", lsTempKeyString, "\n\t-->value: ", lnFileSize)
        lcAlreadyDownloadedFileDictionary[lsTempKeyString] = lnFileSize

# Save dictionary back out to file
# Create backup
if os.path.isfile(lsBackupFileName):
    os.remove(lsBackupFileName)

shutil.copyfile(lsLogFileName, lsBackupFileName)

# write current dictionary. Use io.open() to avoid charmap codec can't encode errors
with io.open(lsLogFileName, 'w', encoding="utf-8") as lcNewLogFileHandle:
    # print(lcAlreadyDownloadedFileDictionary, file=lcNewLogFileHandle)
    for lsKey in lcAlreadyDownloadedFileDictionary.keys():
        laCurrentKeySplit = lsKey.split('?')
        lsTempString = laCurrentKeySplit[0] + ',' + str(lcAlreadyDownloadedFileDictionary[lsKey])
        print(lsTempString, file=lcNewLogFileHandle)

# Print stats
print("\nSUMMARY:")
print("NEW: ", lnNewFiles)
print("Dup: ", lnDupFiles)
print("TOTAL: ", lnNewFiles + lnDupFiles)
# done
