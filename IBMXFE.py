# Requesting input of an ip address.

print("This tool will query the IBM X-Force Exchange API and provide a formatted URL Report.")
iprequested = input("Please enter an IP address: ")

# Defining a callable function with an IP address as an input.

def URLReport(IP):

    # Importing required libraries.

    import urllib.request
    import urllib.error
    import base64
    import re
    import textwrap

    # Defining variables for the API's username and password.

    apiusername = 'c9d292fa-e5b5-4ccb-a3be-7487288cbf19'
    apipassword = '2dd5689d-b4d8-4e87-82fc-a09595e0c9e2'

    # Creating the token from the username and password, then a bytes literal version, and finally converting to base 64 and then back to a string.

    token = apiusername + ':' + apipassword
    tokenbytes = token.encode('utf-8')
    token64 = base64.b64encode(tokenbytes, altchars=None)
    token64string = token64.decode('utf-8')

    # Creating a headers dictionary.  Adding entries for authorization and requested format.

    headers = {}
    headers['Authorization'] = 'Basic ' + token64string
    headers['Accept'] = 'application/json'

    # Code to get a response from the API, convert it to a readable format, and what to do with errors.
    
    try:
        baseurl = 'https://api.xforce.ibmcloud.com/url/'         # Defining the base url
        url = baseurl + IP                                       # Combining the base url with the ip address
        req = urllib.request.Request(url, headers=headers)       # Defining a request variable that includes the url and header information
        resp = urllib.request.urlopen(req)                       # Opening the url                                 
        textbyte = resp.read()                                   # Storing the output
        text = textbyte.decode('utf-8')                          # Converting to a string

        # Converting the text response to a readable format

        print('\nRequest successful...\n')
        URLreturned = re.search('"url":"(.+?)",', text)          # Displaying the returned url
        print('URL: ' + URLreturned.group(1))
        score = re.search(r'"score":([^"]*),', text)             # Displaying the score
        print('Score: ' + score.group(1))

        catsplit1 = text.split('"categoryDescriptions":{')       # Isolating the category information
        cattext1 = catsplit1[1]
        catsplit2 = cattext1.split('}')
        cattext = catsplit2[0]
        cats = re.findall(r'"([^"]*)":', cattext)                # Making a list of categories
        descs = re.findall(r':"([^"]*)"', cattext)               # Making a list of descriptions
        
        catdict = {}                                             # Creating a dictionary for categories and descriptions
        x = 0
        for eachName in cats:                                    
            catdict[eachName] = descs[x]
            x+=1                   
        if catdict == {}:                                        # Printing message if no categories exist
            print('\nNo categories are associated with this URL')
        else:
            print('\nURL Categories: \n')
            for i in catdict:                                    # Printing each pair if they exist
                catdesc = i + ': ' + catdict[i]
                print(textwrap.fill(catdesc) + '\n')             # Using textwrap for more orderly display
                
    # Providing reason and code if error.

    except urllib.error.URLError as e:
        print('\nThere was an error processing your request...\n')
        print('Reason: ',e.reason)
        print('Code:   ', e.code)

# Using the URLReport function with the user requested address.

URLReport(iprequested)
