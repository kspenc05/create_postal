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

def get_town_name(s):
    return s[0] + s[1:].decode('utf-8').lower().split(",")[0]
    
#the Rogers web connection 
rogers = mechanize.Browser()
rogers.set_handle_robots(False)
rogers.set_handle_refresh(False)
rogers.addheaders = [('User-agent', 
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


#the zip-codes.com web connection
zipcode = mechanize.Browser()
zipcode.set_handle_robots(False)
zipcode.set_handle_refresh(False)
zipcode.addheaders = [('User-agent', 
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

zipcode.open('https://www.zip-codes.com/canadian/province.asp?province=on')


#so the script can resume from where it left off from the last time it was ran
with open("checkpoint.txt", "r+") as checkpoint:
    town_num = int(checkpoint.readline())
    postal_num = int(checkpoint.readline())
    total = int(checkpoint.readline())
    
#checking each postal code, based on the combinations created
with open("checkpoint.txt", "w") as checkpoint, open("checked.txt", "a+") as checked:
    #total time spent checking postal codes:
    beg = time.time()
    
    links = zipcode.links()[32:-17]
    for i in range(town_num, len(links)):
        town = links[i]
    
        place_name = get_town_name(town.text)
        print place_name + "\n"
    
        zipcode.follow_link(town)
    
        #print br.links()[27:]
    
        postals = zipcode.links()[27:-17]
        for j in range(postal_num, len(postals)):  
            postal = postals[j].text
            print postal + "\n"

            #by default, split() will split words based on spaces, 
            #we are splitting based on spaces here
            words = postal.split()

            #timer so the server thinks my bot is a human or at least not a pest
            time.sleep(5)
        
            resp = check_postal(rogers, words[0] + " " + words[1])
            
            #to communicate with the user the progress the checker has made
            print words[0] + " " + words[1], ",", place_name, resp
            print "total: ", total, "\nJust checked:",  words[0], " ", words[1], "\n ", place_name, " time running: ", datetime.datetime.fromtimestamp(time.time() - beg) 
            
            postal_num += 1
            total += 1
            
            #NOTE: all that should be in checkpoint at any given time is
            # town number, the number of previously checked postal codes for that
            # town, and then the total number of postal codes checked
            checkpoint.seek(0)
            checkpoint.truncate()
            checkpoint.write(str(town_num) + "\n")
            checkpoint.write(str(postal_num) + "\n")
            checkpoint.write(str(total) + "\n") 
            
            checked.write(words[0] + " " + words[1] + "," + place_name + resp + "\n")
        postal_num = 0
        town_num += 1