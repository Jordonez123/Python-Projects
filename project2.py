#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 13:14:52 2019

@author: jordonez
"""
##this program asks the user to pick a meal of pizza or salad
def select_meal(): 
    print('To end order, enter "done"')
    order = 'You ordered '
    meal_str = ''
    meal_list = []
    m = ''
    
    while meal_str != 'done':
        meal_str = input('Hello, would you like pizza or salad?: ')
        if meal_str == 'pizza':
            pizza_str = pizza() #calling the pizza function, stores returned value in a variable
            meal_list.append(pizza_str)
            m = ' and '.join(meal_list) #adds ' and ' between every element in meal_list,stores it as a string
            print(order + m + '. Place another order or say "done."')
        if meal_str == 'salad':
            salad_str = salad()
            meal_list.append(salad_str)
            m = ' and'.join(meal_list)
            print(order + m +'. Place another order or say "done."')
    print()
    print('Your order has been placed. Goodbye.')
    
def pizza():
    size_str = input('Small medium or large?: ')
    x = 'a {} pizza{}'.format(size_str, toppings()) #calling the toppings() function and using the returned value in the {}
    #print(x)
    return x
    
def salad():
    salad_str = input('Would you like a garden salad or greek salad: ')
    z = ' a {} with {} dressing'.format(salad_str,dressing()) #calling the function dressing and stores the returned value in {}
    #print(z)
    return z
    
def toppings():   
    toppings_str = ''
    toppings_list = [] #empty list to store the user's toppings choices
    while toppings_str != 'done': #asking the user to pick a toppings as long as they don't say 'done' 
        toppings_str = input('Add a topping: pepperoni, mushrooms, spinach, or say done: ')
        if toppings_str != 'done': #checks if user is done with adding toppings
            toppings_list.append(toppings_str) 
    l = ' with ' + ' and '.join(toppings_list) #makes a string of every element in the toppings_list and adds 'and' between every element
    #print(l)
    if len(toppings_list) == 0: #checking if the user only wants a pizza with no toppings
        return '' #if the toppings list is empty (user wants no toppings, then return an empty string)
    return l #returns the string composed of elements in the toppings_list
    
    
def dressing():
    dressing_str= input('Please choose a dressing: vinaigrette, ranch, blue cheese, lemon: ')
    return(dressing_str)

select_meal() #calls the funct