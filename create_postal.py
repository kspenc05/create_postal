#!/usr/bin/python

#In order to run:
#    change file permissions by typing "chmod u+x create_postal.py"
#    then, "./create_postal.py postalCodes.txt", every time after

#Use this script, if you want to receive all possible last three digits of a 
#postal code containing three letters

#to run enter as the second argument, the file where the first halves of
#the postal codes (eg. "L4M, B8J, G5G, F3F") are (eg. "myPostal.txt").

import sys

# PURPOSE:: writes to file all number, letter, number combinations 
#eg. 0A0 excluding the letters 'W' and 'Z'. 
# ARGUMENTS:: the line of the file, and the file object.
def write_combinations(entry, file):
    
    chars = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 
            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y')
        
    nums = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    
    for i in nums:
        for j in chars:
            for k in nums:
                file.write(entry + ' ' + i + j + k + "\r\n")
    file.write("\n\n\n")
    
with(open(sys.argv[1], 'r')) as file:
    codes = file.readlines()
    
#creates new file, since this file might not exist
with(open(sys.argv[1] + "combos", 'w+')) as output:
    for line in codes:
        if(len(line) > 1):
            write_combinations(line.strip('\r\n'), output)