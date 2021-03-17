# -*- coding: utf-8 -*-
"""
@author: Nicholas Ippedico, Nick Braga, Alec Mitchell
"""
import csv, DatabaseManager
class FileManager:
    def __init__(self, dbm):
        self.data={}
        self.dbm = dbm
        
    #loads the csv file
    def load_csv(self, fn):
        with open(fn) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            keys = []
        
            flight_counter = 0 #increment when we see a valid flight
        
            for row in csv_reader:
                if line_count == 0:
                    #replace spaces with dashes
                    
                    for i in range(len(row)):
                        #print('DEBUG: i =', i)
                        keys.append(row[i].replace(' ', '_'))
                        
                    #print('DEBUG: keys =', keys)
                    line_count += 1
                else:
                    flight_id = row[0]
                    if flight_id.isnumeric():
                    
                        flight = {}
                        #iterating with index
                        #print("DEBUG: line =",linenum)
                        if (len(row) < len(keys)):
                            continue
                        #print('DEBUG: row=', row)
                        for i in range(len(row)):
                            #print('DEBUG: i=', i)
                            try:
                                flight[keys[i]] = row[i]
                            except(IndexError):
                                #print('DEBUG: i=', i)
                                pass
                        self.dbm.create_flight(
                            flight['ID'],
                            flight['Airline'],
                            flight['Location'],
                            flight['Date'],
                            flight['Time'],
                            flight['SeatingChoice'],
                            flight['AirlineMiles'],
                            flight['Price']
                            )
                        flight_counter += 1
                line_count += 1
            print('loaded', flight_counter, 'flights from', fn) 
              
    #saves selected data to csv file
    def save_csv(self,fn):
        # select all the data in the database
        #self.dbm.select_all()
        with open(fn,mode='w') as outfile:
            self.dbm.print_selection_to_file(outfile)  
        print('saved flights to', fn)
                        

            
if __name__ == '__main__':
    import DBManager2
    dbm = DBManager2().DatabaseManager()
    dbm.reset()
    fm = FileManager()
    fm.load_csv('flights.csv')
    dbm.select_by_id(['22'])
    fm.save_csv('test.csv')