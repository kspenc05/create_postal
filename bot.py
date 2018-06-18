#!/usr/bin/python
import mechanize
import time
import datetime

#PURPOSE:: to change 't's into "Y"s and 'f's into "N"s, the comma is added at the end 
#since this response will be outputted to a comma delimited text file.
def getYorN(string):
    #The "true" in the string that rogers returns will always start
    # with a lowercase 't', I've checked, don't change this. 
    if string == 't':
        return "Y,"
    else:
        return "N,"

#PURPOSE:: to check if a given postal code is serviced by rogers
#ARGUMENTS:: the web connection, and the postal code.
#RETURNS:: the response from Rogers, formatted so that each value is separated
#by a comma (for a comma delimited file)
def check_postal(br, code):
    br.open("http://www.rogers.com/consumer/internet")
    br.select_form(nr = 0)
    
    check_postal = br.forms()[0].controls[0]
    check_postal.readonly = False
    check_postal.value =  code
    print code

    # returns the required yes or no responses (if given true or false) and whether
    # the postal code is incorrect or not.
    resp = br.submit().read()
    print resp
    
    #some variables to hold each character in the string, where each truth value (T or F) 
    # is related to that service provided by rogers. eg. if tv == 't', then 
    # tv is offered by Rogers at that postal code area else if tv == 'f' it is not. 
    tv = resp.find(":") + 1
    home = resp.find(":", tv) + 1
    internet = resp.find(":", home) + 1
    wrong_postal = resp.find(":", internet) + 1
    
    #Since the part of the response containing "ultimate Internet" will always 
    #be at the end of the string
    if(resp[:-6] == 't'):   
        ultimate = resp[-6]
    else:
        ultimate = resp[-7]
    
    return ( "," + getYorN( resp[tv] ) + getYorN( resp[home] ) +  
        getYorN( resp[internet] ) + getYorN( resp[wrong_postal] ) + 
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
    
    #I assumed that the number of links will not change, this is the reason I 
    #used negative indexes. If those change, these number literals will need to change. 
    links = zipcode.links()[32:-17]
    
    for i in range(town_num, len(links)):
        town = links[i]
        zipcode.follow_link(town)
        
        place_name = get_town_name(town.text)
        print place_name + "\n"
        
        #These 2 lines below are To fix the previous problem where it would crash when 
        # there were more than 1 area code, and it would think one of the area 
        # codes is a postal code
        start = 27
        while(len(zipcode.links()[start].text) != 7): start += 1
        
        postals = zipcode.links()[start:-17]
        
        for j in range(postal_num, len(postals)):  
            #when no arg is given, split() will split words based on spaces
            #NOTE:: I also got rid of previous print command, 
            # because it would print the postal code twice on the screen
            words = postals[j].text.split()

            #timer so the server thinks my bot is a human or at least not a pest
            time.sleep(5)
        
            resp = check_postal(rogers, words[0] + " " + words[1])
            
            #to communicate with the user the progress the checker has made
            print words[0], " ", words[1], ",", place_name, resp
            print "total: ", total, "\nJust checked:",  words[0], " ", words[1], "\n ", place_name, " time running: ", datetime.datetime.fromtimestamp(time.time() - beg), "\n"
            
            postal_num += 1
            total += 1
            
            #NOTE: all that should be in the checkpoint file at any given time is the
            # town number, the number of previously checked postal codes for that
            # town, and then the total number of postal codes checked
            
            #Whenever it writes to this file, it clears everything before it,
            #which is why I used truncate()
            checkpoint.seek(0)
            checkpoint.truncate()
            checkpoint.write(str(town_num) + "\n" + str(postal_num) + "\n" + str(total) + "\n") 
            
            checked.write(words[0] + " " + words[1] + "," + place_name + resp + "\n")
        postal_num = 0
        town_num += 1