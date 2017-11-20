import os
import subprocess

SOURCE_DIR = '/var/ww/folder/folder_goc/'
DESTINATION_FILE = '/var/www/folder/global.log'
LOG_FILE = 'adict.txt'

def doTail(n, sf, df):
    # Copy lines from after line n from sf to df
    count = 0;
    dfh = open(df, 'a') # Create file handler to append new line to df
    try:
        p = subprocess.Popen(['tail', '-n', '+' + str(n), sf], stdout=subprocess.PIPE)
        new_lines = p.communicate()[0].split("\n")
        for line in new_lines:
            dfh.write(line); # write line to dfh handler
        dfh.close()
        return len(new_lines)
    except subprocess.CalledProcessError:
        return -1
    return count # count is equal to the number of lines is copied to df

def loadDict(f):
    s = open(f, 'r').read()
    adict = eval(s)
    return adict

def saveDict(f, adict):
    target = open(f, 'w')
    target.write(str(adict))

copied_file = loadDict(LOG_FILE)
source_files = os.listdir(SOURCE_DIR)
for file in source_files:
    lines_copied = 0
    if file in copied_file:
        lines_copied = doTail(copied_file[file], SOURCE_DIR + file, DESTINATION_FILE) 
        if lines_copied == -1: # Fail
            print("Could not copy file")
            break
        else:
            copied_file[file] += lines_copied # Update after copying, next time, we start from line after this
    else:
        lines_copied = doTail(copied_file[file], SOURCE_DIR + file, DESTINATION_FILE)
        if lines_copied == -1: # Fail
            print("Could not copy file")
            break
        else:
            copied_file[file] = lines_copied # Create new record, next time, we start from line after this
saveDict(LOG_FILE, copied_file)
