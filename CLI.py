# -*- coding: utf-8 -*-
"""
@author: Nicholas Ippedico, Nick Braga, Alec Mitchell
"""
import DatabaseManager, Filemanager

#try:
    #f = open('flightsinput.txt', 'r')    
    #def input(prompt=''):
        #print(prompt, end='')
        #return f.readline().strip()
#except(FileNotFoundError):
    #pass

class CLI():
    
    def __init__(self, dbm):
        self.dbm = dbm
        self.fm = Filemanager.FileManager(dbm)
        
    def run_cli(self):
    
    #menu = input()
    #tokens = menu.split()
    #print('DEBUG:', tokens)

        while True:

            menu = input()
            tokens = menu.split()
            #print('DEBUG:', tokens)
         
            if tokens[0] == 'exit':
                break
            elif tokens[0] == 'create':
               try:
                   print(self.dbm.create_flight(tokens[1], tokens[2], tokens[3],
                                         tokens[4], tokens[5], tokens[6],
                                         tokens[7], tokens[8]))
               except(IndexError):
                   print('Flight creatation: not enough parameters')
            elif tokens[0] == 'select_by_id':
               print(self.dbm.select_by_id(tokens[1]))
            elif tokens[0] == 'select':
                #print("DEBUG:",tokens)
                try:
                    print(self.dbm.select(tokens[1],tokens[2]))
                except(IndexError):
                    print('Flight selection: not enough parameters')
            elif tokens[0] == 'open_flights':
                #print("DEBUG:",tokens)
                print(self.dbm.select('SeatingChoice','OPEN'))
            elif tokens[0] == 'takes_miles':
                #print("DEBUG:",tokens)
                print(self.dbm.select('AirlineMiles','YES'))
            elif tokens[0] == 'location':
                #print("DEBUG:",tokens)
                try:
                    print(self.dbm.select('Location',tokens[1]))
                except(IndexError):
                    print('Flight selection: not enough parameters')
            elif tokens[0] == 'airline':
                #print("DEBUG:",tokens)
                try:
                    print(self.dbm.select('Airline',tokens[1]))
                except(IndexError):
                    print('Flight selection: not enough parameters')
            elif tokens[0] == 'date':
                #print("DEBUG:",tokens)
                try:
                    print(self.dbm.select('Date',tokens[1]))
                except(IndexError):
                    print('Flight selection: not enough parameters')
            elif tokens[0] == 'price':
                #print("DEBUG:",tokens)
                try:
                    print(self.dbm.select('Price',tokens[1]))
                except(IndexError):
                    print('Flight selection: not enough parameters')
            elif tokens[0] == 'time':
                #print("DEBUG:",tokens)
                try:
                    print(self.dbm.select('Time',tokens[1]))
                except(IndexError):
                    print('Flight selection: not enough parameters')
            elif tokens[0] == 'filter':
                #interactive functionality
                """
                print("Which airline?")
                airline = input()
                print("What Location?")
                location = input()
                print("What Date?")
                date = input()
                print("What time?")
                time = input()
                print("Seating Choice?")
                seat = input()
                print("Takes miles?")
                miles = input()
                print("Price?")
                price = input()
                print(self.dbm.filter(airline, location, date, time, seat, miles, price))
                """
                try:
                    print(self.dbm.filter(tokens[1],tokens[2],tokens[3],tokens[4],tokens[5],tokens[6],tokens[7]))
                except(IndexError):
                    print('Flight selection: not enough parameters')
            elif tokens[0] == 'select_all':
               print(self.dbm.select_all())
            elif tokens[0] == 'print_selection':
                self.dbm.print_selection()
            elif tokens[0] == 'load_csv':
                self.fm.load_csv(tokens[1])
            elif tokens[0] == 'save_csv':
                self.fm.save_csv(tokens[1])
            elif tokens[0] == 'reset':
                print(self.dbm.reset())
            elif tokens[0] == 'delete':
                print(self.dbm.delete(tokens[1]))
            else:
                print('invalid command')
        
        
            

def main():
    dbm = DatabaseManager.DatabaseManager()
    cli = CLI(dbm)
    cli.run_cli()
    
main()


