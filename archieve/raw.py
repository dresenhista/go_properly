#import attrs
import os
import regex as re
import pandas
import jason


#function to clean screen
def cls():
	os.system("cls")

#function to remove the failed files
def filter_names(string, pattern):
	filtered = filter(lambda i: not pattern.search(i), string)
	return filtered



#function to all read files
def load_files(path):
	regex = re.compile(".failed")
	#create the list of files
	filenames = filter_names(os.listdir(path), regex) 
	for fname in filenames:
		with open(path+'//'+fname) as infile:
			output.append(infile)

filenames = filter_names(os.listdir(path), regex) 
for fname in filenames:
	with open(path+'\\'+fname) as infile:
		 
		for line in infile.read():
			my_data += line



path = "Scraper/scraped_data"



#text_file = open("output.txt", "w")
#text_file.write(my_data)
#text_file.close()



#function to read a file

file= open("scraped_data\\k=1177309X3H53&p=DE-48119127-83.attrs")
my_data = file.read()