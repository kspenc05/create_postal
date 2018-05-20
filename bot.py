#!/usr/bin/python
import os
import mechanize
import time
import datetime

def getYorN(string):
    if string == 't':
        return "Y,"
    else:
        return "N,"

def check_postal(br, code):
    br.open("http://www.rogers.com/consumer/internet")
    #print  list(br.forms())[0]

    br.select_form(nr = 0)
    check_postal = br.forms()[0].controls[0]

    check_postal.readonly = False
    print code
    check_postal.value =  code

    resp = br.submit().read()
    
    # returns the required yes or no responses (if given true or false) and whether
    # the postal code is incorrect or not.
    
    print resp
    
    tv = resp.find(":") + 1
    home = resp.find(":", tv) + 1
    internet = resp.find(":", home) + 1
    wrong_postal = resp.find(":", internet) + 1
    
    if(resp[:-6] == 't'):
        ultimate = resp[-6]
    else:
        ultimate = resp[-7]
    
    return ( "," + getYorN( resp[tv:tv + 1] ) + 
        getYorN( resp[home:home + 1] ) +  
        getYorN( resp[internet: internet + 1] ) + 
        getYorN( resp[wrong_postal: wrong_postal + 1] ) + 
        getYorN( ultimate ) )
    
#br.form["postalCode-1423593432005"] = 'L1M 7B6' # This does the input
#br.submit() # This will submit the form
#print resp.response().read() 

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.addheaders = [('User-agent', 
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#so the script can resume from where it left off from the last time it was ran
with open("checkpoint.txt", "r+") as checkpoint:
    start = int(checkpoint.readline())
    
#checking each postal code, based on the combinations created
with open("combinations.txt", "r") as file, open("checkpoint.txt", "w") as checkpoint, open("checked.txt", "a+") as checked:
    lines = file.readlines()
    
    #total time spent checking postal codes:
    beg = time.time()

    for i in range(start, len(lines)):
        line = lines[i]
        words = line.split()
        
        if(len(words) > 1):
            #timer
            start = time.time()
            time.clock()
            elapsed = 0
            
            while(time.time() - start < 5): pass
        
            resp = check_postal(br, words[0] + " " + words[1])
            
            print words[0] + " " + words[1], ",", words[2], resp
            print "total: ", i, "\nJust checked:",  words[0], " ", words[1], "\n ", words[2], " time running: ", datetime.datetime.fromtimestamp(time.time() - beg) 
            i += 1
            
            #NOTE: all that should be in checkpoint at any given time is the variable 'i'
            #it is just a marker of progress, to signify what was the last 
            #line of the combinations file it stopped at, hence truncate() is used
            checkpoint.seek(0)
            checkpoint.truncate()
            checkpoint.write(str(i) + "\n")
            
            checked.write(words[0] + " " + words[1] + "," + words[2] + resp + "\n")
            
    #check_postal(br, "N1N 2C4")