# create_all_tables.py
# Create all tables in the Rwandan Law database
# Group: Ctructure
# Date: 10/28/2017

import mysql.connector as mc
from mysql.connector import errorcode
import sys

# define user connection
config = {
    'user': 'kherring',
    'password': '12faye',
    'host': '0.0.0.0',
    'database': 'rwandanlaw'
}

tables = {}
tables['agencies'] = (
    """
    CREATE TABLE agencies (
    abbrev varchar(15) NOT NULL,
    long_name varchar(255) NOT NULL,
    PRIMARY KEY (abbrev)
    ) ENGINE=InnoDB
  """
)

tables['articles'] = (
    """
    CREATE TABLE articles (
    law_id int(10) NOT NULL,
    article_num int NOT NULL,
    article_text varchar(5000) NOT NULL,
    name varchar(500) NOT NULL,
    PRIMARY KEY (law_id, article_num),
    FOREIGN KEY (law_id)
    REFERENCES laws (law_id)
    )
"""
)

tables['cites'] = (
    """
    CREATE TABLE cites (
    reference_id int(10) NOT NULL AUTO_INCREMENT,
    parent_law_num varchar(35) NOT NULL,
    parent_law_date date NOT NULL,
    cited_law_num varchar(35) NOT NULL,
    cited_law_date date NOT NULL,
    PRIMARY KEY (reference_id)
    )
    """
)

tables['content_type'] = (
    """
    CREATE TABLE content_type (
    name varchar(35) NOT NULL PRIMARY KEY,
    authority int NOT NULL
    )
    """
)

tables['drafted_by'] = (
    """
    CREATE TABLE drafted_by (
    law_id int(10) NOT NULL,
    agency varchar(15) NOT NULL,
    PRIMARY KEY (law_id, agency),
    FOREIGN KEY (law_id)
    REFERENCES laws(law_id),
    FOREIGN KEY (agency)
    REFERENCES agencies(abbrev)
    )
    """
)

tables['laws'] = (
    """
    CREATE TABLE laws (
    law_id int(10) NOT NULL AUTO_INCREMENT,
    law_num varchar(35),
    exact_date date NOT NULL,
    name varchar(500) NOT NULL,
    ending varchar(1000) ,
    intro varchar(5000) NOT NULL,
    content_type varchar(35) NOT NULL REFERENCES contents(content_type),
    pub_id int(10) NOT NULL,
    INDEX (law_num, exact_date),
    FOREIGN KEY (pub_id)
    REFERENCES publications(pub_id),
    PRIMARY KEY (law_id)
    )
    """
)

tables['publications'] = (
    """
    CREATE TABLE publications (
    pub_id int(10) NOT NULL AUTO_INCREMENT,
    var_num varchar(10) NOT NULL,
    name varchar(55) NOT NULL,
    pub_date date NOT NULL,
    INDEX (var_num, pub_date),
    PRIMARY KEY (pub_id)
    ) ENGINE=InnoDB
  """
)

tables['repeals'] = (
    """
    CREATE TABLE repeals (
    repeal_id int(10) NOT NULL AUTO_INCREMENT,
    parent_law_num varchar(35) NOT NULL,
    parent_law_date date NOT NULL,
    impacted_law_num varchar(35) NOT NULL,
    impacted_law_date date NOT NULL,
    PRIMARY KEY (repeal_id)
    )
    """
)
tables['users'] = (
    """
    CREATE TABLE users (
    username varchar(30) NOT NULL,
    email varchar(20) NOT NULL,
    password varchar(15) NOT NULL,
    first_name varchar(15) NOT NULL,
    last_name varchar(15) NOT NULL,
    PRIMARY KEY(username)
    )ENGINE=InnoDB
   """
)

try:
    cnx = mc.connect(**config)
    cursor = cnx.cursor()
    #exit()
except mc.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Err: Access Denied (Verify user and password)")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database not found")
    else:
        print(err)
    sys.exit(1)

needed = dict(tables)  # all tables need to be created
while needed:
    for name, cmd in tables.iteritems():
        if name in needed:  # not already successfully created in loop
            try:  # create table
                print("Creating table {}:".format(name))
                cursor.execute(cmd)
                print("OK")
                del needed[name]  # success
            except mc.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("ALREADY EXISTS")
                    del needed[name]
                else:
                    print(err.msg)

cursor.close()
cnx.close()
