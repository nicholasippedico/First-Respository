# -*- coding: utf-8 -*-
"""
@author: Nicholas Ippedico, Nick Braga, Alec Mitchell
"""
import sqlite3

class DatabaseManager:
    
    def __init__(self):
        #creates sql database
        self.conn = sqlite3.connect('flights.db')
        
        #creates table with values
        self.__execute_query('''CREATE TABLE IF NOT EXISTS flights
                        (ID integer UNIQUE,
                         Airline text,
                         Location text,
                         Date integer,
                         Time text,
                         SeatingChoice text,
                         AirlineMiles text,
                         Price integer)''')
        
        #getting the cloumn names
        query = "PRAGMA table_info(cars);"
        rows = self.__execute_query(query) # a database row is a list of tuples
        #self.col_names
        
        self.col_names = [row[1] for row in rows]
    #closes the database
    def __del__(self):
        #closes the connect when it is done.
        self.conn.close()
        
    #checks the submitted values
    def __check_attr(self, attr):
        if attr in self.col_names:
            return True
        return False
    
    #gets the column names 
    def get_col_names(self):
        return self.col_names
    
    #gets row names
    def get_rownames(self): 
        return self.rows
    
    #resets the database table to a blank table and recreates an empty table
    def reset(self):
        #Drop the table
        self.__execute_query("DROP TABLE IF EXISTS flights")
        #call constructor to set up the table again
        self.__init__()
        
        #
        return ("reset database")
    
    #execute query function
    def __execute_query(self, query, params=None):
        
        c = self.conn.cursor()
        
        #execute the query
        if not params:
            c.execute(query)
        else:
            c.execute(query, params)
        
        #get results of query, rows is a list of tuples    
        rows = c.fetchall()
        #commit changes
        self.conn.commit()
        
        return rows
    
    #selects all flight data stored in the table
    def select_all(self):
        query = '''SELECT * from flights'''
        
        self.rows = self.__execute_query(query)
        
        return("selected all {} flights".format(len(self.rows)))
    
    #selects a flight by the flight ID
    def select_by_id(self, ID):
        query = '''SELECT * from flights WHERE id = ?'''
        
        self.rows = self.__execute_query(query, (ID,))
        
        #an empty list is False, when evaulated as a bool
       
        if not self.rows:
            return(1, "select: flight {} not found".format(ID))
        else:
            return ("selected flight {}".format(ID))
        
    #selects flight info based on user given attributes 
    def select(self, attr,val):
        
        
        attr = attr.replace('-', '_')
        
        self.conditions = []
        #self.conditions is a list of tuples, initialized to [] in __init__()
        self.conditions.append((attr, val))
        
        #selects flights with specific values in specific rows
        query = ('''SELECT * from flights WHERE ''' + attr + ''' LIKE ''' + '''"%''' + val + '''%"''')        
        
        self.rows = self.__execute_query(query)
        
        
        if not self.rows:
            print(attr, val, "not found")
        
        return('selected ' + str(len(self.rows)) + ' flights with ' + attr + ' ' + val)
        
    #filter function to search for flights that meet all user given criteria
    def filter(self, airline, location, date, time, seat, miles, price):
        
        query = ('''SELECT * from flights WHERE Airline ''' 
                 + ''' LIKE ''' + '''"%''' + airline + '''%"''' + ''' AND Location '''
                 + ''' LIKE ''' + '''"%''' + location + '''%"''' + ''' AND Date  '''
                 + ''' LIKE ''' + '''"%''' + date + '''%"'''+ ''' AND Time '''
                 + ''' LIKE ''' + '''"%''' + time + '''%"'''+ ''' AND SeatingChoice '''
                 + ''' LIKE ''' + '''"%''' + seat + '''%"'''+ ''' AND AirlineMiles '''
                 + ''' LIKE ''' + '''"%''' + miles + '''%"'''+ ''' AND Price '''
                 + ''' LIKE ''' + '''"%''' + price + '''%"''')        
        
        self.rows = self.__execute_query(query)
        
        
        if not self.rows:
            print("There are no flights that match these parameters")
        
        return('selected ' + str(len(self.rows)) + ' flights')
        
         
    #print selected data
    def print_selection(self, args=None):
        query = 'PRAGMA table_info(flights);'
        infos = self.__execute_query(query)
        count = 1
        #print(infos)
        col_names = list(info[1] for info in infos)
        #col_names = list(info[1] for info in infos)
        for row in infos:
            col_names.append(row[1])
            
            
        if self.rows:
            print('selection:')
        else:
            print('print_selection: no selection to print')
            
        for row in self.rows:
            print('\t'+ str(count))
            count+=1
            for i in range(len(row)):
                print('\t' + str(col_names[i]) + ':' + str(row[i]))

    #saves the selected data to a new csv file           
    def print_selection_to_file(self, fh, args=None):
        #query = 'PRAGMA table_info(flights);'
        #infos = self.__execute_query(query)
        
        #print(infos)
        col_names = ['ID', 'Airline', 'Location', 'Date', 'Time', 
                     'SeatingChoice', 'AirlineMiles', 'Price']
        #col_names = list(info[1] for info in infos)
        #for row in infos:
            #col_names.append(row[1].replace('_', ' ').capitalize())
        #col_names[0] = col_names[0].upper()
        fh.write(','.join(col_names)) 
        fh.write("\n")
               
        for row in self.rows:
            for i in range(len(row)):
                fh.write(str(row[i]))
                if(i != len(row)-1):
                    fh.write(',')
            fh.write("\n")
        #    fh.write(','.join(row))

    
    #creates a new flight
    def create_flight(self, ID, airline, location, date, time, seatingchoice, airlinemiles, price):
        
        #(ID, make, model, year, body) = tuple(args)
        args = (ID, airline, location, date, time, seatingchoice, airlinemiles, price)
        if (args[0].isnumeric()):
            pass
        else:
            return (0, 'create: invalid parameter(s)')
        query = '''INSERT INTO flights (ID, Airline, Location, Date, Time, SeatingChoice, AirlineMiles, Price)
            VALUES( ?, ?, ?, ?, ?, ?, ?, ?); '''
        
        try:
            self.__execute_query(query, tuple(args))
            
            return ("created flight with id {}".format(ID))
        except sqlite3.IntegrityError as e:
            return (0, str(e))
          
    #deletes a flight with the given flight ID
    def delete(self, ID):
        query = '''SELECT * from flights WHERE id = ?'''
        
        found = self.__execute_query(query, ID)
        
        if not found:
            return(0, 'delete: flight ' + str(ID) + ' not found')
        
        query = '''DELETE FROM flights WHERE ID=?'''

        self.__execute_query(query, ID)

        return ('deleted flight {}'.format(ID))
    
    