#!/usr/bin/python

import subprocess

#Use underscores for multiple words, PLEASE! It is based on command line args
for L in ('K', 'L', 'M', 'N', 'P'):
    with open("Ontario_" + L, "r") as postals, open("rurals_" + L, "r") as rurals:
        for line in postals.readlines():
            words = line.split()
            
            if(len(words) > 1):
                #print words[0], words[1]
                subprocess.call("./create_postal.py " + words[0] + " " + words[1], shell = True)
        
        for line in rurals.readlines():
            words = line.split()
            
            if(len(words) > 1):
                subprocess.call("./create_postal.py " + words[0] + " " + words[1], shell = True)