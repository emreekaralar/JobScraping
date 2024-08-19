# JobScraping


Open up the terminal and paste:

pip install beautifulsoup4 scrapy pandas openpyxl requests

this will install the necessary libraries 

Please change the location where you want to save the excel file for each code

For amazon and microsoft, once you download the files, open up the terminal and type:


For Amazon:

cd amazon

cd amazon

scrapy runspider amazon_jobs.py


For Microsoft:

cd microsoft

cd microsoft

scrapy runspider microsoft_jobs.py


For Google:

Create a new file and paste the code available under google.py

run the script 


For Meta:

Go to : https://www.metacareers.com/jobs?sort_by_new=true 
1- Right click

2- Inspect

3- Go to network tab

4- Reload the page

5- Find the file named graphql, there should be couple of them, find the one where it starts with {"data":{"job_search":["id". Once you find the right file go to preview and copy value job search, create a new json file in python, paste it there and save the file. Then go to excel and open with that json file, go to power query and reformat the data and it's done.
