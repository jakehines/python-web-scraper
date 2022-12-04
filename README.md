# python-web-scraper

This is a simple Python web scraper.  Its purpose is to expose a beginner to Python and some common functions.

## Dependencies
This script is dependent on the requests library used to request the HTML document and lxml for parsing the resulting document.

## Instructions
This is an exercise in using Python.  The script will access a wikipedia page and parse out informtion from a table.  The webpage is https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal). 
It is recommended that you have this page opened in Chrome or Firefox in inspect element while following along in the activity.  Any time a comment references the HTML or HTML elements, it is pointing
the reader towards the code in question in the inspect element view.  This is so you can visualize why the parsing is done as it is.

The code is not meant to be up to a commercial level of quality.  The activity is meant for beginners and takes several roundabout ways to accomplish a task in order to illustrate the way algorithms or 
data structures are implemented and used in Python.

While you are following along, you should think about ways this can be improved.  Also experiment with things you can access.  Run the code often so you know it works to a certain point.

## Assignment
Write a Python script which can parse the main table at https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal).  The output should be a .csv with comma separated values and newlines separating the 
records.  Each record should contain the country's rank, name and UN GDP estimate from the table.

## Follow on assignment Idea
Generalize the script to read all tables from a given wikipedia url.  The script should take in the URL a parameter and parse all availble data from all tables into a separate csv. 
All file names should be based on the name of the table and columns should be names correctly.

Note: this follow on is a lot more involved than the simple script attached.  The goal is that by completing the assignment, you will know enough about how the data is structured in these markup languages
to create a better and more generalized script.