#!/usr/bin/env python3
# networkFileRW.py
# Roger Schoverling
# 28 MArch 2023
# updated: 03 April 2023

## change log
# 1. Use equip_r.txt Download equip_r.txt to read the routers and addresses
#    into a dictionary in the networkFileRW program.
# 2. Use equip_s.txt Download equip_s.txtfile to read the switches and
#    addresses into a dictionary in the networkFileRW program.
# 3. Modify the networkFileRW.py file to include a try/except clause for
#    importing the JSON module.
# 4. Use constants for the equip_r.txt file and the equip_s.txt file and
#    your output files (name one updated.txt, the other is invalid.txt).
# 5. Use the syntax on the slides for reading a JSON file and writing a JSON
#    file.
# 6. In the summary, write the updated dictionary to the updated.txt file, but
#    print the number of devices updated on the screen.
# 7. Write the invalidIPAddresses list to the errors.txt file. Print the number
#    of bad addresses on the screen.
# 8. The rest of the program will be identical to GPA 6.


##---->>>> Use a try/except clause to import the JSON module
try:
    # I added sys so I could have a graceful exit if the exception failed.
    import sys
    import json
except:
    print('Either the JSON or sys moduled failed to import.',
          'Check your Python 3 instalation and try again!')
    input('Press enter to exit the program.')
    sys.exit()

##---->>>> Create file constants for the file names; file constants can be reused
##         There are 2 files to read this program: equip_r.txt and equip_s.txt  
ROUTERS_FILE    = 'equip_r.txt'
SWITCHES_FILE   = 'equip_s.txt'
##         There are 2 files to write in this program: updated.txt and errors.txt
UPDATED_FILE    = 'updated.txt'
ERRORS_FILE     = 'errors.txt'

#prompt constants
UPDATE          = "\nWhich device would you like to update "
QUIT            = "(enter x to quit)? "
NEW_IP          = "What is the new IP address (111.111.111.111) "
IP_INVALID      = 'Sorry, that is not a valid IP address!\n'
IP_CHAR_ERROR   = 'Invalid input - no letters or characters.\n'
R_FILE_ERROR    = f'The file {ROUTERS_FILE} is missing!'
S_FILE_ERROR    = f'The file {SWITCHES_FILE} is missing!'

#function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

#function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        #print("octets", octets)
        for byte in octets:

            # ensure the octet is valid
            try:
                # convert the byte into an integer 
                byte = int(byte)
                # make sure the ip address has exactly 4 octets 
                # and current byte has a value from 0 to 255 (8-bit).
                if len(octets) != 4 or byte < 0 or byte > 255:
                    # when not valid rase an exception
                    raise UserWarning

            except UserWarning:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                #inform the user
                print(IP_INVALID)
                # start over at the IP prompt
                break

            except:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                #inform the user
                print(IP_CHAR_ERROR)
                # start over at the IP prompt
                break
            
        else:
            #validIP = True
                return ipAddress, invalidIPCount
                #don't need to return invalidIPAddresses list - it's an object
        
def main():

    ##---->>>> open files here
    #dictionaries
    try:
        ##---->>>> read the routers and addresses into the router dictionary
        with open(ROUTERS_FILE) as r:
            routers = json.load(r)
            #print(routers)
    except FileNotFoundError:
        print(R_FILE_ERROR)
        routers = {}

    try:
        ##---->>>> read the switches and addresses into the switches dictionary
        with open(SWITCHES_FILE) as s:
            switches = json.load(s)
            #print(switches)
    except FileNotFoundError:
        print(S_FILE_ERROR)
        switches = {}

    #the updated dictionary holds the device name and new ip address
    updated = {}

    #list of bad addresses entered by the user
    invalidIPAddresses = []

    #accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    #flags and sentinels
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:

        #function call to get valid device
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        #function call to get valid IP address
        #python lets you return two or more values at one time
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        #update device
        if 'r' in device:
            #modify the value associated with the key
            routers[device] = ipAddress 
            #print("routers", routers)
            
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        #add the device and ipAddress to the dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)
        #loop back to the beginning

    #user finished updating devices
    print("\nSummary:\n")

    ##---->>>> write the updated equipment dictionary to a file
    with open(UPDATED_FILE, 'w') as e:
        json.dump(updated, e)
        print("Number of devices updated:", devicesUpdatedCount)

    print("Updated equipment written to file 'updated.txt'\n")

    ##---->>>> write the list of invalid addresses to a file
    with open(ERRORS_FILE, 'w') as e:
        json.dump(invalidIPAddresses, e)
        print("Number of invalid addresses attempted:", invalidIPCount)

    print("List of invalid addresses written to file 'errors.txt'")

    input('Press the ENTER key to exit!')

#top-level scope check
if __name__ == "__main__":
    main()




