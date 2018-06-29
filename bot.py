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
    
    #Whether or not there was an error when getting the data is far more important
    #than if the postal code was in the incorrect format or wrong (it seems like it just checks format,
    #not if the postal code is used by someone living in Ontario). 
    error = resp.find(":", internet) + 1
    error = resp.find(":", error) + 1
    
    #Since the part of the response containing "ultimate Internet" will always 
    #be at the end of the string
    #changed it so that the variable is the index, not the letter anymore
    if(resp[:-6] == 't'):   
        ultimate = -6
    else:
        ultimate = -7
    
    return ( getYorN( resp[tv] ) + getYorN( resp[home] ) +  
        getYorN( resp[internet] ) + getYorN( resp[error] ) + 
        getYorN( resp[ultimate] ) )

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
#Each of the three values needed is on a separate line, so it reads them in 
#converts each, and assigns it to a variable. 
with open("checkpoint.txt", "r+") as checkpoint:
    town_num, postal_num, total = [int(i) for i in checkpoint.readlines()]
    
#checking each postal code, based on the combinations created
with open("checkpoint.txt", "w") as checkpoint, open("checked.txt", "a+") as checked:
    #start of the running time spent on checking postal codes:
    beg = time.time()
    
    #I assumed that the number of links will not change, this is the reason I 
    #used negative indexes. If those change, these number literals will need to change. 
    links = zipcode.links()[32:-17]
    
    for i in range(town_num, len(links)):
        place_name = get_town_name(links[i].text)
        print place_name + "\n"
        
        zipcode.follow_link(links[i])
        
        #To fix an error where no postal codes or area codes appear,
        # if there are no area codes, then there are no postal codes, so then it
        # should move to the next municipality in the list.
        if(zipcode.links()[26].text == "Canadian Postal Code Database"):
            continue
        
        #These 2 lines below are To fix the previous problem where it would crash when 
        # there were more than 1 area code, and it would then think one of the area 
        # codes IS a postal code
        start = 27
        while(len(zipcode.links()[start].text) != 7):
            start += 1
            
        postals = zipcode.links()[start:-17]
        
        for j in range(postal_num, len(postals)):
            
            #timer so the server thinks my bot is a human or at least not a pest
            time.sleep(5)
            
            #when no arg is given, split() will split words based on spaces
            #NOTE:: I also got rid of previous print command, 
            # because it would print the postal code twice on the screen
            words = postals[j].text.split()
            resp = check_postal(rogers, words[0] + " " + words[1])
            
            #to communicate with the user the progress the checker has made
            print words[0], " ", words[1], ",", place_name, ",", resp
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
            checkpoint.write("%s\n%s\n%s\n" % (str(town_num), str(postal_num), str(total)))
            
            checked.write("%s %s,%s,%s\n" % (words[0], words[1], place_name, resp))
        postal_num = 0
        town_num += 1