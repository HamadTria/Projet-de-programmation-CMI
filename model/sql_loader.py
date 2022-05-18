import csv, sqlite3

con = sqlite3.connect('./model/ABunchOfTrees.db', check_same_thread=False)
cursor = con.cursor()

def get_connexion():
    return con

def get_csv_in_df(pd):
    return pd.read_csv('./model/Repro_IS.csv', sep=';')

def tableInitialize():
    #Creation of the 'Valley' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS valley (
            Id_ INTEGER PRIMARY KEY AUTOINCREMENT,
            Valley TEXT NOT NULL,
            Latitude REAL,
            Longitude REAL
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
            Longitude REAL,

            Valley_id INTEGER NOT NULL,
            FOREIGN KEY (Valley_id) REFERENCES valley(Id_)
        );
    ''')

    #Creation of the 'Tree' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tree (
            Id_ INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            Species TEXT, 
            VH REAL,
            H REAL,
            SH REAL,

            Station_id INTEGER NOT NULL,
            FOREIGN KEY (Station_id) REFERENCES station(Id_)
        );
    ''')

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
            rate_Germ REAL,

            Tree_id INTEGER NOT NULL,
            FOREIGN KEY (Tree_id) REFERENCES tree(Id_)
        );
    ''')

def databaseInitialize():
    with open('./model/Repro_IS.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        #We get the names of our tables.
        table_names = [names[0] for names in cursor.execute('SELECT name FROM sqlite_master WHERE type = \'table\' AND name NOT LIKE \'sqlite_%\';').fetchall()]
        #We get the name of the columns of each table and we store it in a dictionary.
        columns_names = {table_name: [names[0] for names in cursor.execute('SELECT name FROM pragma_table_info(\'{}\');'.format(table_name)).fetchall()[1:]] for table_name in table_names}

        Last_id = 0 #Save the id of the current table for the foreign key of the next table.
        for row in reader:
            for table_name in table_names:
                #We check if the first field are the same.
                query = 'SELECT Id_, {0} FROM {1} WHERE {0} IS ?;'.format(columns_names[table_name][0], table_name)
                
                checkIfExist = cursor.execute(query, (row[columns_names[table_name][0]], )).fetchone()

                if not checkIfExist is None:
                    Last_id = checkIfExist[0]
                    continue

                #We modify the current row to replace the 'NA' by None according to the table.
                rows = list(map(row.get, columns_names[table_name]))
                rows = list(map(lambda x: None if x in ['NA', 'NA ', ''] else x, rows))
                if table_name != 'valley':
                    rows[-1] = Last_id

                query = 'INSERT INTO {} ({}) VALUES '.format(table_name, ', '.join(columns_names[table_name]))
                query += '({});'.format(', '.join(['?' for i in columns_names[table_name]]))

                cursor.execute(query, rows)
                Last_id = cursor.lastrowid

        con.commit()

def databaseAddCoordinate():
    with open('./model/Lat-Long_byStation.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            query = 'UPDATE Station SET {} = ? WHERE Station="{}" AND Station IS NULL;'.format(' = ?, '.join(['Latitude', 'Longitude']), row['Station'])
            
            rows = list(map(row.get, ['Latitude', 'Longitude']))

            cursor.execute(query, rows)
        con.commit()