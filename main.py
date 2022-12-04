#-------------PYTHON WEB SCRAPER------------------
# this is a python project written for a beginner
# programmer to begin to understsand how to use 
# python and some of its most common features
#-------------------------------------------------
# We will do this by completing a simple exercise
# where we will request the webpage for a wikipedia
# page and parse a table from it to a csv file
# ------------------------------------------------
# a good follow on exercise would be to adapt this
# script to take a wikipedia url as a parameter and parses all
# tables from the page and outputs to "table_name.csv"

#SPECIFIC ASSIGNMENT:
#Parse the HTML document elements of the wikipedia page found at https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal) for the
#main table containing the list of countries and gdp.  Dump the data found in this table to a csv file which contains the country name, and UN Estimate
#for GDP, where each record is separated by a new line (\n) and the column are separated by a comma (,)

#packages
import requests #used to send http requests over the internet
from lxml import etree #used to parse markup documents like xml and html
from io import StringIO, BytesIO

#STEP 1: OBTAIN DOCUMENT TREE FOR THE WIKIPEDIA PAGE------------------------------------------
# for this we will be hardcoding all links and paths
# we will be parsing the data from the table on this:
# https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)
# take a minute to look at the table

#request the page
page_url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
#send the GET request
#this is the same type of request you send when using the URL bar on the browser
#store the response of the request in "response"
print("Sending GET request to {}".format(page_url)) #logging
response = requests.get(page_url)

#the response will contain a number of standard parts
#defined by http
#the first area of interest is the RESPONSE CODE https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

#this is easy to handle using our RESPONSE object

res_code = response.status_code

#logic based on response code, look at the linked webpage to see why the logic is such

if res_code > 299: #any code 300 or up means there was an error
    #exit in the case of an error requesting
    print("Error: Recieved response code of {}. Exiting.".format(res_code))
    exit()

#will continue here if no error with request
print("Success: Recieved response from URL of {}.".format(res_code))
#>>>should be 200


#next lets look at the headers
#there is a DICTIONARY for response.headers
#this dictionary is indexed by words
#one standard field is the 'content-type'
#which tells you what type of data you recieved
content_type = response.headers['content-type']
print("Request response content type: {}".format(content_type))
#>>>text/html; charset=UTF-8
#since we have a html doc, we know we
#can parse the html elements for table data

#first lets store the document in variable
doc = response.text
# if you printed doc, you should see html code
# like you would if you inspected element on the 
# webpage in your browser

#STEP 2: FIND AND STORE THE TABLE IN SOME DATATYPE FOR EASY PARSING-----------------------------------------------------------
#use the "doc" string of html code and push it in
#the contruector for ELEMENTTREE parser

parser = etree.HTMLParser()                 #create a HTMLParser object to pass to the etree.parse method, otherwise, it will default to the xml parser
tree = etree.parse(StringIO(doc),parser)    #parse the doc, typing it as a StringIO and giving it the correct parser

html_root = tree.getroot() #passes html raw text into html parser
                                     #this will take that text and organize it
                                     #into a data type that is easy to access
                                     #data from
                                     #the returned value is the "root" of the
                                     #markup doc

# markup docs use a heirarchy, which you may have already picked up on
# by viewing the page in inspect element.  You see html elements contain 
# other elements, which is where the "heirarchy" come from
# look at the page in inspect element and see that the tag 
# which looks something like <tag> that contains all the elements
# in the document is the <html> tag.  Notice it is closed at the end of the document
# with </html>.  This is the ROOT of the document

#lets verify that we have what we expect as the root.  
# you can access the name instide the brackes <name> by
# calling the elements .tag field.
print("Starting to parse the HTML doc at root: {}".format(html_root.tag))

#at this point we are ready to parse by accessing children elements of the root
# and by doing logic on the tag names and various fields in the elements:
#   <html>                 <--------root/current element
#        <div class="some_class">some text in here</div>         <------------child of root, this code is also the .text of the root bc it is inside the tags <html>
#   </html>

#in the above example there are some more details that are hard to point out using text art
# "div"- this is an example of an elements TAG
# "class=some_calss" is an attribute.  You can call the elements .attribute which returns a dictionary
# in this example accessing .attribute['class'] will return "some_class"
# "some text in here"- is an example of an elements .text, it will return the stuff inside the tags

#now that we know generally what we use to parse the document, we want to think of a way
#to use these to isolate the table in question.

#there are a number of ways to do this.  
#every element has a unique XPATH.  You can go to the page's inspect element, locat the element containing the 
#entire table, and right click on it and select copy XPATH, then select the table element from our variable using this

#this will work for ouR page, but if we want to expand it to other pages, the XPATH will need to be manually copied and pasted
#into the program, so we wont be using this approach

#instead, look at the various tags, attributes and text, to see how we can uniquely identify the table. 
#looking at the element in inspect element, we see the entire table is contained by:
# <table class="wikitable sortable static-row-numbers plainrowheaders srn-white-background jquery-tablesorter" border="1" style="text-align:right;">
#   ^       ^                                                                                                       ^                   ^
#   TAG     |                                                                                                      attribute          attribute
#          attribute

#At this point, there are many ways we can parse for this element. 
#The best way to do this would be to write an algorithm which can parse *any* table from a wikipedia page
#However, this is something I'd like to leave as an exercise for the reader.

#inside the library we are using, there are methods for searching the element tree for things, but we
#are going to skip these.  The approach we are using is not very general and is meant to show how to 
#access things.

#So, I'm going to hardcode the parsing through the child elements of root, so the reader can see how to 
#access the information we need to write the above mentioned algorithm.  

#Starting to code again, we are going to use the last line of code we typed, which is the root.
#Looking in the page's inspect element in browser, we can see the CHILD's of the root, which is <html>
#If you collapse everything in the inspect element page that is inside the <html> tags, you will see two
#elements one level below, namely: <head> and <body>

#We want to trace down this hirarchy to the table.

#If we review where the <table> element is, we can see it is inside the <body> somewhere so we want to select this

# calling root.child returns an array of these elements
#[<head>,<body>]
#           ^ Want this one, at index 1 of the array
#We will use a variable to reference our CURRENT ELEMENT, and keep changing it is referencing our <table> object

#We get the root elements children by directly indexing the element we wnat its children of, remember we want the child at index 1
curr_elem = html_root[1]

#verify that we have the body in curr_element
tag = curr_elem.tag
print("Parsing inside element: {}".format(tag))

#now I repeat the process.  Look back in inspect element, and look at which element one level down from <body> contains the table

#looking at the document, we see it is the element defined by 
#<div id="content" class="mw-body ve-init-mw-desktopArticleTarget-targetContainer" role="main">
#        ^
#        |
#       this is an attribute for this element called "id" with a value of "content"

#If you use the indexing method we used before, you would see that this is the child element of 
# curr_elem located at index 2, or is the third child element.  We could use this to get the child
# which contains the element, exactly as we did with root, but for the sake of exercise, we are going
# to use a different approach

#this element contains an attribute called "id".  In web page code, this id is exceptionally
# useful because it is meant to be a unique identifier for the element.  If we look at id="content" we
# know that this <div> is the only element with this id.

#So, lets iterate through the childeren of curr_elem = <body> until we find the element 

for child in curr_elem: #starts at index 0->curr_elem.size assinging curr_elem[i] to child
    #if we tried to access the id attribute of a child element, and it didn't have one in the doc,
    #the program would crash when it tries to access it

    #Lets print info for the start of the loop and do comparisons later
    #Tag name is easy to access
    tag = child.tag
    
    #now we need to make sure we don't crash the script if we try to check the id on an element which doesn't have one
    if(not child.attrib['id']): #if the attrib at index id doesn't exist
        #verify information
        print("Checked element: {} with no ID.".format(tag))
        continue
    
    #at this point we know that an id exists
    id = child.attrib['id']

    #verify information
    print("Checking element: {} with ID: {}".format(tag,id))
    if(not child.tag == "div"): #check if child's tag is "div"
        continue
    #Because an element could theoretically have any number of attributes and values for those attributes,
    #attributes are stored as a dictionary, indexed by the name of the attribute.  In our case, the name of the 
    #attribute is "id"
    attributes = child.attrib
    id = attributes['id']

    if(not id == "content"): #ensure the id is "content"
        continue

    #if it makes it to this point in the loop, it means the tag of the child is "div"
    #and the id is "content", so we will assign curr_elem to this new element, to continue parsing
    curr_elem = child
    break                   #this is an akward way of doing this, but if this code was in a method, a "break" could be accomplished via the "return" statement (future improvement for reader?)

tag = curr_elem.tag
id = curr_elem.attrib['id']
#now lets verify that we have the correct element
print("Parsing inside element: {} with ID: {}".format(tag,id))

#So now we've parsed two layers down in our tree or "heirarchy"
# We used the first approach where we knew which position the
# child element was at, and directly referenced it.

#We also iterated through the children until we found the id
#of the element we wanted.  Remember we can do this because an 
# elements id is unique.

#This script is not at all generalized, but when you go to do that
#you will absolutely need to write your own funtion library
#To get some practice with this, lets write a function to get a child object
#by its ID

#This is probably already implemented in the "lxml" library, but again, its for the sake of exercise

#Since we are hardcoding everything, we are going to code this function without providing any protection
#if there is no child element with id="whatever we want".  Validating that this happens and providing an
#exception would be ideal, but this will be an exercise for the reader and we will just be careful to use it 
#only on elements we know have an id="something"

def get_child_by_id(element,id):  #we need to pass the element in since we are not writing a method for its class
    #this could be implemented via the same logic as above, but I am providing a more concise way of doing this
    #iterate through the child elements
    for child in element:
        #try catch to access its id without verifying it exists
        try:
            child_id = child.attrib['id']
            #check that the id is what we want
            if(child_id == id):
                return child  #return the child and exit the function
        except:
            continue
        
#we can see pretty clearly that this function will return nothing if there is no
#child with id=id.  You could imagine that this will cause issues if we try to use 
#this function in this case.  Try to imagine how you could handle this exception.

#Now that we have that function, lets look forward to see the next level in the tree
#we need to go to in order to access our <table>

#recall we are at element curr_elem=<div id="content">
#we can see that the next element directly below, has an id attribute, so we can use 
#the function we just wrote to reference it.  

#By look at inspect element on the page we cans see the child which contains the <table> is:
# <div id="bodyContent" class="vector-body">

#so lets pass the id into our function with current element
curr_elem=get_child_by_id(curr_elem,"bodyContent")

#and verify that the correct element was assigned to our curr_elem
tag = curr_elem.tag
id = curr_elem.attrib['id']
print("Parsing inside element: {} with ID: {}".format(tag,id))

#so now we've drastically shortened the amount of code we need to trace down the 
#stack of elements.  

#From here down to the <table> element, we can use our function for every
#child element which has an id.

#Looking back at inspect element, we can see the child of curr_elem=<div id="bodyContent"> which
#contains the <table> as an ID of "mw-content-text"
#so again, lets get this element by its id and assign it to curr_elem
curr_elem = get_child_by_id(curr_elem,"mw-content-text")

#and verify that we having it
tag = curr_elem.tag
id = curr_elem.attrib['id']
print("Parsing inside element: {} with ID: {}".format(tag,id))

#we can see the next element has no ID, so our function will not work
#instead because <div id="mw-content-text"> has relatively few children,
#we are just going to use inspect element to see that it is the 0'th child
#element that contains our <table> and access it similarly to above

curr_elem=curr_elem[0]

#and verify that this is the desired element
tag = curr_elem.tag
class_name = curr_elem.attrib['class']
print("Parsing inside element: {} with class {}".format(tag,class_name))
#and at last, we see the <table> is a direct child of curr_elem=<div class="mw-parser-output">
#unfortunatly, it does not have an ID, so our function will not work on it.
#if we try to look for <table> elements, this could return multiple tables, as 
#curr_elem has multiple <table>s as children.

#we can see that the detail which separates it is the "class" which has a really long name as its value
# <table class="wikitable sortable static-row-numbers plainrowheaders srn-white-background jquery-tablesorter"> 

#the class is an attribute just like ID is.  However, a class attribute is often used by the css and javascript running
#on a webpage to make the page function.  This means that a class does not need to be unique.  There can be multiple elements
#of the same class.  However, elements with the same function or appearance are potential candidates for sharing a class,
#and the table of interest is the only element on the page which looks and functions as it does.  So, we can be pretty confident
#that there are probably no other elements on the page that share the class.  Even if there were, we will just be parsing the children of our
#curr_elem.

#we are just going to bank on selecting by the class name being a reliable way of getting this table.
#since it is a main variable we will be referencing, we are going to store the table in a new varible

table = None
for child in curr_elem: #parse the children of curr_elem
    try:
        #try to access the class name, will throw exception if no class attribute
        class_name = child.attrib['class']
        #"return" the table if it matches our desired class name
        if class_name == "wikitable sortable static-row-numbers plainrowheaders srn-white-background":
            table = child
    except:
        continue

#and verify that the table is correct

tag = table.tag
class_name = table.attrib['class']

print("Found table at [{}] with class [{}]".format(tag,class_name))

#So what we've done:
#Using inspect element to understand how we could parse
#this specific page and find a reference to the table object

#STEP 3: EFFICIENTLY PARSE THE DATA FROM THE TABLE------------------------------------------------------------------------------------------

#notice: the table title and the various column headings are things
#that you would probably need to access to make a generalized table parser.

#since we are only accessing some of the data, I will leave it as an exercise to the reader 
#to access the various and standard elements which contain details about the table's title and column names.

#to efficiently parse this, we would ideally loop through all of the data 1 time.
#this means access the data and dump to file for each record.
#this is opposed to accessing the data into a table-like array then looping
#over that to dump into file

#so lets start parsing
#we can see the data is stored in a child element of <table> called <tbody>

#lets select this one
for child in table:
    try:
        if child.tag == "tbody":
            table = child
    except:
        continue

#and verify
print("Located table data at element: {}".format(table.tag))

#tables in HTML are already sort of in a data frame.
#we can see that inside the <tbody> there is exclusivley
#child elements called <tr> which stands for "table row"
#each of these is a record we need to parse.

#notice, we can see two <tr>'s which have a "class" attribute.
#these are the two rows that have non-countries, namely "World" and 
# the EU entries.  For the sake of exercise, we will exclude these.

#the way we exclude them is by definig a function to determine if 
#the <tr> has a "class" attrib, so we know when to exclude it.

def has_class(element):
    #verify it has attributes
    if not element.attrib:
        return False
    #verify it has a class attribute
    if not element.attrib['class']:
        return False
    #return true if it does
    return True

#in order to dump to a file, we need to create said file.
#it will also be useful to append to this file as we iterate through the table.

#so lets create a file with the appropriate column headings

with open("output.csv","w+") as f: #with open opens the file, "w+" means we will be writing to it, and the + means to create the file if it doesn't exist
    column_titles = "rank,country,estimated_gdp\n"
    f.write(column_titles)
#before we get too into the parsing, we need to consider some issues

#the first is that there isn't a UN estimate in the table for every country.
#The second is that when estimates are missing, there is only one <td> taking 
# up two columns in the table.

#this second issue will make indexing which <td> has the correct estimate difficult. We can't hardcode
#the 7th column or 6 index because that isn't the case when data is missing in earlier rows.

#first lets solve how to find out if an estimate is missing

def has_data(element): #we will pass in a <td> as the element
    #there are numerous things about these elements that tell us that they don't contain data
    #here we will look inside the element to see if its value is "—"
    if element.text == "—":
        return False
    else:
        return True

#now lets define a function to return the expected index of the UN Estimate in a row
#knowing that there could be empty data colums

def index_of_estimate(row):
    #for keeping track:
    #0- name
    #1- region
    #2- IMF Estimate
    #3- IMF date
    #4- world bank estimate
    #5- world bank year
    #6- un estimate
    #7- un year

    #so lets start with our expected index=6 and subtract 1
    #for each column with missing data, to account for the missing <tr>

    #we know country name and region won't be missing, so lets start inspecting
    #the elements at index 2

    index = 2
    est_index = 6

    #next, lets use our above function to determine if the node is empty
    if(has_data(row[index])):
        #if it has data, we want to move two ahead and check if the next one is empty
        index += 2
    else:
        #if it doesn't have data we need to accont for the missing <tr>
        est_index -=1
        #and move only one <tr> and check if its empty
        index += 1
    
    #check the next estimate
    if(has_data(row[index])):
        return est_index
    else:
        return est_index-1





#now we can begin parsing the table row by row
#make a variable to store the rank:
rank = 1
for row in table:
    #first want to continue if it is one we want to skip
    if has_class(row):
        continue
    
    #now that we know we have a row we want to include, lets look at the HTML to see how to access the information we want
    #you can see the children of the <tr> are <td>'s which stand for "table data". 

    #we know the country name will be the 0th <td> in the row
    name_element = row[0]
    #remember, this returns the element containg the country name, not the name in text
    #to get that we actually need to access another element inside the <td> with tag <a>
    
    #we can see that things are arranged by country flag element then name element, so the <a>
    #element is always at index 1

    name_element = name_element[1]

    #inside this elements .text is the country name
    name = name_element.text

    #next we will use our index_of_estimate method to access the correct estimate
    est_index = index_of_estimate(row)

    #access estimate
    est_element = row[est_index]

    #the estimate could be missing, but assuming we have its index, we can grab its
    # text, if it exists, it will store the number, if it doesn't it will grab the "—"
    #either way this will work

    estimate = est_element.text
   
    #this estimate will contain commas, which will mess up the csv format, so we need to remove them

    estimate = estimate.replace(",","") #replaces commas with nothing

    #now that we have the rank, name, and gdp estimate, 
    # we are ready to append them to our csv

    with open ("output.csv","a") as f:
        csv_record = "{},{},{}\n".format(rank,name,estimate)
        f.write(csv_record)

    #Verify that the data was added
    print("Appended data to file:")
    print("     Rank: {}".format(rank))
    print("     Country: {}".format(name))
    print("     GDP: {}".format(estimate))

    #remember to iterate the rank
    rank += 1

#and we have completed parsint the table
print("Successfully completed parsing the table.")
exit()
    