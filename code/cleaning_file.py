#import attrs
import os
import regex as re
import pandas as pd
import xlsxwriter
import json
import csv


#to install a library in python in windows :(
#python -m pip install library

#function to clean screen I use windows :(
def cls():
	os.system("cls")


#read file
file_raw= open("Scraper\\scraped_data\\k=1177309X3H53&p=DE-48366643-872.attrs")
file_raw = file_raw.read()
file = json.loads(file_raw)

#pandas is able to read dictionary type data if they are not nested (which our is)
#let's try to unest the data before
def unnest_dictionary(file):
	data_list = []
	for address, info in file.iteritems():
	  info['base_description'] = ''
	  info['rooms'] = ''
	  info['Address'] = address
	  data_list.append(info)
	return data_list



#clean the weird number columns that we dont know what they do
# we know they follow a number only naming
def clean_column_numbers(df):
	df = df[df.columns.drop(list(df.filter(regex='^([0-9][0-9]{0,2}|1000)$')))]
	return df






#select columns that we want to use
# we will be using to start the following columns: 

def select_columnc(df):
	df = df[['Sold Price', 'Basement Development','Baths Full', 'Beds Total', 'Building Type', 'Community', 'Construction Type', 'Exterior', 'Front Exposure', 'Goods Included', 'Heating Fuel', 'List Price', 'Parking', 'Property Type',  'Style', 'Tax Amount', 'Tot Flr Area A.G. (SF)', 'Total Parking', 'Yr Built', 'day_sold', 'dom', 'postal_code']]
	return df


###################################################################################
#all the numeric data are assigned as string so we need to convert them first
#function to convert string in number
def num_convertor(df, column_name):
	df[column_name] = df[column_name].replace('[\$,]', '', regex=True).astype(float)
	return df[column_name]




#writting all variables to be converted
def convert_columns(df):
	var_to_convert = ['Sold Price', 'Baths Full',
	'Beds Total', 'Tax Amount', 'List Price', 'Beds Total','Tot Flr Area A.G. (SF)', 'Total Parking', 'dom']
	#looping through variables
	for item in var_to_convert:
		df[item] = num_convertor(df, item)
	return df

def clean_data_function(file):	
	data_list = unnest_dictionary(file)
	df = clean_column_numbers(pd.DataFrame(data_list))
	#define postal code
	df['postal_code'] = df['Address'].str[-7:]
	df = select_columnc(df)
	#deleting rows when it's empty sold price
	df = df[df['Sold Price']>1]
	df = convert_columns(df)
	return df




#remove the non attrs files
def filter_names(mylist, pattern):
	r = re.compile(pattern)
	newlist = filter(r.match, mylist)
	return newlist

#function to all read files 
#translate them in df and export a csv
def load_files(path):
	regex = re.compile(".*attrs")
	#create the list of files
	filenames = filter_names(os.listdir(path), regex) 
	index=1
	for fname in filenames:
		file_raw= open(path+'//'+fname)
		file_raw = file_raw.read()
		file = json.loads(file_raw)
		df = clean_data_function(file)
		df.to_csv('Scraper\\new_data\\file_'+str(index)+'.csv')
		index=index+1
			
	return df


load_files('Scraper//scraped_data')