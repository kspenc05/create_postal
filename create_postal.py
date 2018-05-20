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
def write_combinations(entry, file, location):
    digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    
    [file.write(entry + ' ' + i + j + k + " " + location + "\r\n") 
        for i in digits
        for j in ('A', 'B', 'C', 'E', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 
            'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z') 
        for k in digits]
    file.write("\n")
    
#creates new file, since this file might not exist
with open("combinations.txt", 'a+') as output:
    write_combinations(sys.argv[1], output, sys.argv[2])