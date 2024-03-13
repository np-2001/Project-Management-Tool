import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import datetime

#Citation: Learned the correct syntax for parameterized query
#https://stackoverflow.com/questions/775296/mysql-parameterized-queries

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'

    def query(self, query = "SELECT CURDATE()", parameters = None):

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

    def about(self, nested=False):    
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info



    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        

        if purge:
            self.query(query="DROP TABLE IF EXISTS skills;")
            self.query(query="DROP TABLE IF EXISTS experiences;")
            self.query(query="DROP TABLE IF EXISTS positions;")
            self.query(query="DROP TABLE IF EXISTS institutions;")
            self.query(query="DROP TABLE IF EXISTS feedback;")

        #Feedback Table
        with open('flask_app/database/create_tables/feedback.sql','r') as file:
            query_statement = file.read()
            self.query(query=query_statement)
        

        #Institution Table
        with open('flask_app/database/create_tables/institutions.sql','r') as file:
            query_statement = file.read()
            self.query(query=query_statement)

        with open('flask_app/database/initial_data/institutions.csv','r') as file:
            content = list(csv.reader(file))
            table_columns = content[0]
            table_parameters = content[1:]
            self.insertRows(table='institutions',columns=table_columns,parameters=table_parameters)



        #Position Table
        with open('flask_app/database/create_tables/positions.sql','r') as file:
            query_statement = file.read()
            self.query(query=query_statement)

        
        with open('flask_app/database/initial_data/positions.csv','r') as file:
            content = list(csv.reader(file))
            table_columns = content[0]
            table_parameters = content[1:]
            self.insertRows(table='positions',columns=table_columns,parameters=table_parameters)

        #Experiences Table
        with open('flask_app/database/create_tables/experiences.sql','r') as file:
            query_statement = file.read()
            self.query(query=query_statement)       

        with open('flask_app/database/initial_data/experiences.csv','r') as file:
            content = list(csv.reader(file))
            table_columns = content[0]
            table_parameters = content[1:]
            self.insertRows(table='experiences',columns=table_columns,parameters=table_parameters)

        #Skills Table
        with open('flask_app/database/create_tables/skills.sql','r') as file:
            query_statement = file.read()
            self.query(query=query_statement)

        with open('flask_app/database/initial_data/skills.csv','r') as file:
            content = list(csv.reader(file))
            table_columns = content[0]
            table_parameters = content[1:]
            self.insertRows(table='skills',columns=table_columns,parameters=table_parameters)       

        print('I create and populate database tables.')



    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):

        for parameter in parameters:
            if parameter != []:
                for column in range(len(parameter)):
                    if parameter[column] == 'NULL':
                        parameter[column] = None

                if table == 'institutions':
                    self.query(query="INSERT INTO `institutions` (`inst_id`,`type`,`name`,`department`,`address`,`city`,`state`,`zip`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",parameters=parameter)
                elif table == 'positions':
                    self.query(query="INSERT INTO `positions` (`position_id`,`inst_id`,`title`,`responsibilities`,`start_date`,`end_date`) VALUES (%s,%s,%s,%s,%s,%s)",parameters=parameter)
                elif table == 'experiences':
                    self.query(query="INSERT INTO `experiences` (`experience_id`,`position_id`,`name`,`description`,`hyperlink`,`start_date`,`end_date`) VALUES (%s,%s,%s,%s,%s,%s,%s)",parameters=parameter)
                elif table == 'skills':
                    self.query(query="INSERT INTO `skills` (`skill_id`,`experience_id`,`name`,`skill_level`) VALUES (%s,%s,%s,%s)",parameters=parameter)
                elif table == 'feedback':
                    #Will come back to this
                    pass
        if table == 'institutions':
            #print(self.query(query="SELECT * FROM institutions;"))
            pass
        elif table == 'positions':
            #print(self.query(query="SELECT * FROM positions;"))
            pass
        elif table == 'experiences':
            #print(self.query(query="SELECT * FROM experiences;"))
            pass
        elif table == 'skills':
            #print(self.query(query="SELECT * FROM skills;"))
            pass            
        elif table == 'feedback':
            #Will come back to this
            pass
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
    
        # return {1: {'address' : 'NULL',
        #                 'city': 'East Lansing',      
        #                'state': 'Michigan',
        #                 'type': 'Academia',
        #                  'zip': 'NULL',
        #           'department': 'Computer Science',
        #                 'name': 'Michigan State University',
        #            'positions': {1: {'end_date'        : None,
        #                              'responsibilities': 'Teach classes; mostly NLP and Web design.',
        #                              'start_date'      : datetime.date(2020, 1, 1),
        #                              'title'           : 'Instructor',
        #                              'experiences': {1: {'description' : 'Taught an introductory course ... ',
        #                                                     'end_date' : None,
        #                                                    'hyperlink' : 'https://gitlab.msu.edu',
        #                                                         'name' : 'CSE 477',
        #                                                       'skills' : {},
        #                                                   'start_date' : None
        #                                                 },
        #                                              2: {'description' : 'introduction to NLP ...',
        #                                                     'end_date' : None,
        #                                                     'hyperlink': 'NULL',
        #                                                     'name'     : 'CSE 847',
        #                                                     'skills': {1: {'name'        : 'Javascript',
        #                                                                    'skill_level' : 7},
        #                                                                2: {'name'        : 'Python',
        #                                                                    'skill_level' : 10},
        #                                                                3: {'name'        : 'HTML',
        #                                                                    'skill_level' : 9},
        #                                                                4: {'name'        : 'CSS',
        #                                                                    'skill_level' : 5}},
        #                                                     'start_date': None
        #                                                 }
        #                                             }}}}}
