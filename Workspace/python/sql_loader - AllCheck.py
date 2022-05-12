import csv

def tableInitialize(cursor):
    #Creation of the 'Harvest' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS harvest (
            Id_ INTEGER PRIMARY KEY AUTOINCREMENT,
            ID TEXT NOT NULL,
            harv_num REAL,
            DD REAL,
            harv REAL,
            Year INTEGER,
            Date DATETIME,
            Mtot REAL,
            Ntot REAL,
            Ntot1 REAL,
            oneacorn REAL,
            tot_Germ REAL,
            M_Germ REAL,
            N_Germ REAL,
            rate_Germ REAL
        );
    ''')

    #Creation of the 'Tree' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tree (
            Id_ INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            VH REAL,
            H REAL,
            SH REAL
        );
    ''')

    #Creation of the 'Station' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS station (
            Id_ INTEGER PRIMARY KEY AUTOINCREMENT,
            Station TEXT NOT NULL,
            Range INTEGER NOT NULL,
            Altitude INTEGER NOT NULL,
            Latitude REAL,
            Longitude REAL
        );
    ''')

    #Creation of the 'Valley' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS valley (
            Id_ INTEGER PRIMARY KEY AUTOINCREMENT,
            Valley TEXT NOT NULL,
            Latitude REAL,
            Longitude REAL
        );
    ''')

    #Creation of the 'Links' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            Id_ INTEGER PRIMARY KEY AUTOINCREMENT,

            Harvest_id INTEGER NOT NULL,
            Tree_id INTEGER NOT NULL,
            Station_id INTEGER NOT NULL,
            Valley_id INTEGER NOT NULL,
            FOREIGN KEY (Harvest_id) REFERENCES harvest(Id_)
            FOREIGN KEY (Tree_id) REFERENCES tree(Id_)
            FOREIGN KEY (Station_id) REFERENCES station(Id_)
            FOREIGN KEY (Valley_id) REFERENCES valley(Id_)
        );
    ''')

def databaseInitialize(cursor):
    with open('Repro_IS.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        #We get the names of our tables.
        table_names = [names[0] for names in cursor.execute('SELECT name FROM sqlite_master WHERE type = \'table\' AND name NOT LIKE \'sqlite_%\';').fetchall()]
        #We get the name of the columns of each table and we store it in a dictionary.
        columns_names = {table_name: [names[0] for names in cursor.execute('SELECT name FROM pragma_table_info(\'{}\');'.format(table_name)).fetchall()[1:]] for table_name in table_names}

        for row in reader:
            ids = [] #We get the 'Id_' of the different tables for the 'links' table.
            for table_name in table_names:
                #We modify the current row to replace the 'NA' by None according to the table.
                rows = list(map(row.get, columns_names[table_name]))
                rows = list(map(lambda x: None if x in ['NA', 'NA ', ''] else x, rows))

                query = 'SELECT Id_, {} FROM {} WHERE '.format(columns_names[table_name][0], table_name)
                query += ' IS ? AND '.join(columns_names[table_name])
                
                #We check if all the fields are the same.
                checkIfExist = cursor.execute(query + ' IS ?;', rows if table_name != 'links' else ids).fetchone()

                if not checkIfExist is None:
                    ids.append(checkIfExist[0])
                    continue

                query = 'INSERT INTO {} ({}) VALUES '.format(table_name, ', '.join(columns_names[table_name]))
                query += '({});'.format(', '.join(['?' for i in columns_names[table_name]]))

                cursor.execute(query, rows if table_name != 'links' else ids)
                ids.append(cursor.execute('SELECT Id_ FROM {} ORDER BY Id_ DESC LIMIT 1;'.format(table_name)).fetchone()[0])