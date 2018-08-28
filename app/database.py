import psycopg2
from app.models import User_model,Question_model,Answer_model

class Database:

    def __init__(self):
        self.connection = psycopg2.connect(
            database="stackoverflow_db", user="postgres",  password="1234",host="localhost", port="5432"
        )
        self.cursor = self.connection.cursor()
    
    def create_db_tables(self):
        """creates all the tables for the db"""
        create_table = "CREATE TABLE IF NOT EXISTS userstable\
        ( user_id SERIAL PRIMARY KEY, name VARCHAR(150), username VARCHAR(100) UNIQUE, password VARCHAR(100))"
        self.cursor.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS questionstable\
        (questionid SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, \
        FOREIGN KEY (user_id) REFERENCES userstable (user_id) ON UPDATE CASCADE ON DELETE CASCADE,\
        title VARCHAR(255), body VARCHAR,tag VARCHAR(255), posted_at TIMESTAMP DEFAULT NOW())"
        self.cursor.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS answerstable\
        (answer_id SERIAL PRIMARY KEY, questionid INTEGER NOT NULL, \
        FOREIGN KEY (questionid) REFERENCES questionstable (questionid) ON UPDATE CASCADE ON DELETE CASCADE,\
        content VARCHAR(255), user_id INTEGER NOT NULL, \
        FOREIGN KEY (user_id) REFERENCES userstable (user_id) ON UPDATE CASCADE ON DELETE CASCADE)"
        
        self.cursor.execute(create_table)
        self.connection.commit()
        self.connection.close()

    def insert_user_data(self,name, username, password ):
        """insert user"""
        insert_cmd = "INSERT INTO userstable (name, username, password) VALUES\
         ('{}', '{}', '{}');".format(name, username,  password)
        self.cursor.execute(insert_cmd )
        self.connection.commit()
        

    def get_by_parameter(self, table, column_name,parameter):
        fetch_cmd = "SELECT * FROM {} WHERE {} = '{}';".format(table, column_name, parameter)
        self.cursor.execute(fetch_cmd)
        result = self.cursor.fetchone()
        return result
        

    def get_all(self, table):
        fetchall_cmd = "SELECT * FROM {} ;".format(table)
        self.cursor.execute(fetchall_cmd)
        result = self.cursor.fetchall()
        return result
        
    def insert_question_data(self,title, body, tag ):
        """insert question"""
        insertquestion_cmd = "INSERT INTO questionstable (title, body, tag) VALUES\
         ('{}', '{}', '{}');".format(title, body,  tag)
        self.cursor.execute(insertquestion_cmd )
        self.connection.commit()
