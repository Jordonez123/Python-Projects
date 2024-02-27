#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:22:01 2019

@author: jordonez
"""
##this function reads in the text file "markets.txt" stored in "Documents" and returns two dictionaries
##first dictionary maps zip codes(keys) to lists of farmers market tuples (values)
##second dictionary maps towns (keys) to sets of zip codes (values)

def read_markets(filename):
    filename = open(filename,'r')
    count_hash=0
    line = filename.readline()
    line= line.strip() #strips the \n of each line
    x = 0 ##this keeps track of the position of the hash tags
    a_dict = {} #dictionary mapping zip codes to lists of farmers market tuples
    b_dict = {} ##dictionary mapping towns to sets of zip codes
    zip_code_tuple = set() #creating an empty set
    for line in filename:
        for i in range(0,len(line),1):
            if line[i]=='#':
                x = i 
                count_hash+=1
                if count_hash == 5:
                    break #main loop breaks once the # count is 5, marking the seperation of longitude and latitude entries
                
        info = line[:x] #assigns info to the beginning of the line till that 5th #
        info = info.split('#') #seperates info line at the #s
        zip_code = info[4]
        city = info[3]
        
        market_info = tuple(info[0:5]) #assigns the tuple containing information to market_info
        if zip_code not in a_dict: 
            a_dict[zip_code] = []
        market_list = a_dict[zip_code]
        market_list.append(market_info) #appends the tuple containing market info to market_list
        
        if city not in b_dict:
            b_dict[city] = set() #assigns an empty set to the city "key"
        if zip_code != 'None': #checking to see if the zipcode is 'None'
            zip_code_tuple = b_dict[city]
        zip_code_tuple.add(zip_code) #adds the zip_code to the tuple containin
        
    return a_dict,b_dict
##this function formats a tuple into a human-readable string
def print_market(market):
  
    return "{}\n{}\n{}\n{}, {}{}{}\n{}".format(' ', market[1],market[2],market[3],market[0],' ',market[4],'')
#formatting a tuple using the indexes of the string

if __name__ == "__main__": #creating a main group
    
    FILENAME = "markets.txt" #assigning the file "markets.txt" located in "Documents" 
    try: 
        dictionaries = read_markets(FILENAME) #calls the function read_markets and passes the text file parameter
        a_dict,b_dict = dictionaries
        user_input = input('Please enter a zip code or a town name or quit to exit: ' )
        while user_input != 'quit': 
            if user_input not in a_dict: #cheks if the user input is neither in a_dict or in b_dict
                if user_input not in b_dict: 
                    print('Not found')
            if user_input.isdigit(): #checks if the user input only contains numbers(zipcode)
                if user_input in a_dict:
                    zip_request = a_dict[user_input]
                    for el in zip_request:
                        print(print_market(el))
                        print('')
                            
            if user_input in b_dict:
                town_request = b_dict[user_input] #sets the value associated to the "town key" in b_dict
                for el in town_request: #for every element in the town_request set  of tuplets
                    farmers_markets = a_dict[el] ##assign a single tuplet to "farmers markets"
                    for el in farmers_markets: ##for every zip code in the tuplet 
                        print(print_market(el)) ##print the associated market name 
            
            user_input = input('Please enter a a zip code or a town name: ' ) 
            #keeps asking the user for input until they enter quit

    except (FileNotFoundError, IOError):
        print("Error reading {}".format(FILENAME))
        