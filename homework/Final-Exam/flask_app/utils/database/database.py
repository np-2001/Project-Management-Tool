import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['users','boards','boardgroups','cards']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        ''' FILL ME IN WITH CODE THAT CREATES YOUR DATABASE TABLES.'''

        #should be in order or creation - this matters if you are using forign keys.
         
        if purge:
            for table in self.tables[::-1]:
                self.query(f"""DROP TABLE IF EXISTS {table}""")
            
        # Execute all SQL queries in the /database/create_tables directory.
        for table in self.tables:
            
            #Create each table using the .sql file in /database/create_tables directory.
            with open(data_path + f"create_tables/{table}.sql") as read_file:
                create_statement = read_file.read()
            self.query(create_statement)

            # Import the initial data
            try:
                params = []
                with open(data_path + f"initial_data/{table}.csv") as read_file:
                    scsv = read_file.read()            
                for row in csv.reader(StringIO(scsv), delimiter=','):
                    params.append(row)
            
                # Insert the data
                cols = params[0]; params = params[1:] 
                self.insertRows(table = table,  columns = cols, parameters = params)
            except:
                print(table)
                print('no initial data')


    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        #columns_str = ", ".join(f"`{column}`" for column in columns)
        column_str = ""
        for i in range(len(columns)):
            if i != len(columns)-1:
                column_str += "{},".format(columns[i])
            else:
                column_str += "{}".format(columns[i])


        for parameter in parameters:
            if parameter != []:
                for column in range(len(parameter)):
                    if parameter[column] == 'NULL':
                        parameter[column] = None

                if table == 'users':
                    self.query(query="INSERT INTO `users` ({}) VALUES (%s,%s,%s)".format(column_str),parameters=parameter)
                elif table == 'boards':
                    self.query(query="INSERT INTO `boards` ({}) VALUES (%s)".format(column_str),parameters=parameter)
                elif table == 'boardgroups':
                    self.query(query="INSERT INTO `boardgroups` ({}) VALUES (%s,%s)".format(column_str),parameters=parameter)
                elif table == 'cards':
                    self.query(query="INSERT INTO `cards` ({}) VALUES (%s,%s,%s,%s)".format(column_str),parameters=parameter)
        print('I insert things into the database.')

    




#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):
        password = self.onewayEncrypt(string=password)
        self.insertRows(table='users',columns=['role','email','password'],parameters=[[role,email,password]])
        return {'success': 1}

    def authenticate(self, email='me@email.com', password='password'):
        password = self.onewayEncrypt(string=password)
        count = (self.query(query="SELECT COUNT(*) FROM `users` WHERE email=%s and password=%s",parameters=[email,password])[0]['COUNT(*)'])
        if int(count) > 0:
            return {'success': 1}
        else:
            return {'success': 0}

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message
    
#######################################################################################
# Board RELATED
#######################################################################################

    def CreateBoard(self,name,emails):
        #self.query(query="INSERT INTO `users` ({}) VALUES (%s,%s,%s)".format(column_str),parameters=parameter)
        self.insertRows(table='boards',columns=['board_name'],parameters=[["name"]])
        id = self.query(query="SELECT COUNT(*) FROM boards;")
        parameter_list = []
        for email in emails:
            parameter_list.append([email,id[0]["COUNT(*)"]])
        self.insertRows(table='boardgroups',columns=['user_email','board_id'],parameters=parameter_list)
        return {'success': 1,"id":id}
    
    def GetBoardData(self,board_id):
        board_data = {"id":board_id}
        allowed_emails = self.query(query="SELECT user_email FROM boardgroups WHERE board_id = %s;",parameters=[board_id])

        #[{'user_email': 'nit@email.com'}, {'user_email': 'np@email.com'}]
        board_data["allowed_emails"] = allowed_emails

        cards = self.query(query="SELECT * FROM cards WHERE board_id = %s;",parameters=[board_id])
        board_data["cards"] = cards
        # print(board_data)
        return board_data