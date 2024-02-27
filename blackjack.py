#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 17:37:46 2019

@author: jordonez
"""
#/usr/bin/python
# -*- coding: utf-8 -*-
'''worked and cooperated with Joseph Borison'''
import random
class Card(object):  
    
    def __init__(self, suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return '{}{}'.format(self.suit,self.rank)

    def value(self, total):
        self.total = total
        cd_val_int = 0
        if self.rank.isdigit():
            cd_val_int = int(self.rank)
            #print('cardval: ', cd_val_int)
        else:
            if self.rank in ['J','Q','K']:
                cd_val_int = 10
            elif self.rank == 'A' and (self.total + 11) <= 21:
                cd_val_int = 11
            else:
                cd_val_int = 1
                #print('cardval: ', cd_val_int)
        return cd_val_int # replace this line

def make_deck():
    card_list = []
    suits = ['♠','♣','♦','♥']
    name = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    for i in range (0,len(name),1): #iterating through names
        for a in range(0,len(suits),1): #iterating through suits
            x = suits[a]
            y = name[i]
            card = Card('{}'.format(x),'{}'.format(y))
            card_list.append(card)
    random.shuffle(card_list) #shffles the 'built deck'
    return card_list

def main():
    x = input('Do you want to play a single game of black jack? (y/n): ' )
    if x == 'y':
        deck = make_deck()
        total = 0 #sum
        test_card = deck[0]
        print('You drew', test_card.__str__())
        total += test_card.value(total) #increases value of total by value of first card
        print('sum : ', total)
        deck.remove(deck[0]) #removes first item from deck
        ask_str = input('Do you want another card? (y/n): ' )
        while ask_str != 'n': #while user says yes
        #for i in range (0,len(deck),1):
            top_card = deck[0]
            print('You drew ', top_card.__str__())
            total += top_card.value(total)  #increases value of total by value of drawn card
            print('sum : ', total)
            deck.remove(deck[0]) #removes first picked card
            if total == 21:
                print("You win")
                break
            if total > 21:
               print('You lose')
               break
            if total != 21:
               ask_str = input('Do you want another card? (y/n): ' )
        if total < 21:
            print('My turn.')
            dealer_total = 0
            while dealer_total < total: #makes sure the dealer does not lose due to a lower sum when player 'stays'
                top_card = deck[0]
                print('I drew', top_card.__str__())
                dealer_total += top_card.value(dealer_total)
                print('My sum: ', dealer_total)
                deck.remove(deck[0])
                if dealer_total > total and dealer_total <= 21:
                    print("I win")
                    break
                elif dealer_total == 21:
                    print("I win")
                    break
                elif dealer_total > 21:
                    print("You win")
                    break
                elif total == dealer_total:
                    print("Push! No one wins!")
                    break
    else:
        return 

if __name__ == "__main__":
    main()