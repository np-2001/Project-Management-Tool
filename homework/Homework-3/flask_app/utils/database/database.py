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
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
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

                if table == 'institutions':
                    self.query(query="INSERT INTO `institutions` ({}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)".format(column_str),parameters=parameter)
                elif table == 'positions':
                    self.query(query="INSERT INTO `positions` ({}) VALUES (%s,%s,%s,%s,%s,%s)".format(column_str),parameters=parameter)
                elif table == 'experiences':
                    self.query(query="INSERT INTO `experiences` ({}) VALUES (%s,%s,%s,%s,%s,%s,%s)".format(column_str),parameters=parameter)
                elif table == 'skills':
                    self.query(query="INSERT INTO `skills` ({}) VALUES (%s,%s,%s,%s)".format(column_str),parameters=parameter)
                elif table == 'users':
                    self.query(query="INSERT INTO `users` ({}) VALUES (%s,%s,%s)".format(column_str),parameters=parameter)
        print('I insert things into the database.')

    
    def getResumeData(self):
        # Pulls data from the database to genereate data like this:
        resume_data = {}
        institution_data = self.query(query="SELECT * FROM institutions;")
        for row in institution_data:
            institution_id      = row["inst_id"]
            institution_type    = row["type"]
            name                = row["name"]
            department          = row["department"]
            address             = row["address"]
            city                = row["city"]
            state               = row["state"]
            institution_zip     = row["zip"]


            institution_dict =  {
                                'address' : address,
                                'city': city,      
                                'state': state,
                                'type': institution_type,
                                'zip': institution_zip,
                                'department': department,
                                'name': name,
                                'positions':{}
                            }

            resume_data[institution_id] = institution_dict
        
        #Position
        position_data = self.query(query="SELECT * FROM positions;")
        for row in position_data:
            position_id         = row['position_id']
            institution_id      = row["inst_id"]
            title               = row["title"]
            responsibilities    = row["responsibilities"]
            start_date          = row["start_date"]
            end_date            = row["end_date"]

            position_dict = {'end_date':end_date,'responsibilities':responsibilities,'start_date':start_date,'title':title,'experiences':{}}

            resume_data[institution_id]['positions'][position_id] = position_dict
        
        #Experiences
        experience_data = self.query(query="SELECT * FROM experiences;")

        for row in experience_data:
            experience_id       = row['experience_id']
            position_id         = row['position_id']
            name                = row["name"]
            description         = row["description"]
            hyperlink           = row["hyperlink"]
            start_date          = row["start_date"]
            end_date            = row["end_date"]

            experience_dict = {"description":description,'end_date':end_date,'start_date':start_date,'hyperlink':hyperlink,'name':name,'skills':{}}
            print(position_id)

            for institution_id in resume_data:
                if position_id in resume_data[institution_id]['positions']:
                    resume_data[institution_id]['positions'][position_id]['experiences'][experience_id] = experience_dict
        
        #Skills
        skill_data = self.query(query="SELECT * FROM skills;")
        for row in skill_data:
            skill_id        = row['skill_id']
            experience_id   = row['experience_id']
            name            = row['name']
            skill_level     = row['skill_level']
            
            skill_dict = {'name':name,'skill_level':skill_level}
            for institution_id in resume_data:
                for position_id in resume_data[institution_id]['positions']:
                    if experience_id in resume_data[institution_id]['positions'][position_id]['experiences']:
                        resume_data[institution_id]['positions'][position_id]['experiences'][experience_id]['skills'][skill_id] = skill_dict
                    

        return resume_data



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