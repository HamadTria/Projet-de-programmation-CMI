import csv
from re import S

def sqlInitialize(cursor):
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

    #Creation of the 'Valley' table
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

def dataInitialization(cursor):

    def queryConstructor(str, info, data, ids=[]):
        if ids:
            str = str[:-1] + '{}'.format(tuple(ids))
            return str + ';'

        for i in range(len(data)):
            if data[i] in [None, 'NA', 'NA ', '']:
                str += 'NULL, '
            elif info[i][1] in ['TEXT', 'DATETIME']:
                str += '\'{}\', '.format(data[i])
            else:
                str += '{}, '.format(data[i])
        str = str[:-2]

        return str + ');'

    with open('Repro_IS.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        #We get the names of our tables
        table_names = [names[0] for names in cursor.execute('SELECT name FROM sqlite_master WHERE type = \'table\' AND name NOT LIKE \'sqlite_%\';').fetchall()]
        #We get the name of the columns of each table and we store it in a dictionary
        columns_info = {table_name: [names for names in cursor.execute('SELECT name, type FROM pragma_table_info(\'{}\');'.format(table_name)).fetchall()[1:]] for table_name in table_names}
        columns_names = {table_name: [names[0] for names in values] for table_name, values in columns_info.items()}

        for row in reader:
            ids = []
            for table_name in table_names:
                query = 'INSERT INTO {} {} VALUES ('.format(table_name, '({})'.format(', '.join(columns_names[table_name])))
                if table_name == 'links':
                    query_check = 'SELECT * FROM links WHERE Harvest_id = ? AND Tree_id = ? AND Station_id = ? AND Valley_id = ?;'
                    check = cursor.execute(query_check, ids).fetchone()

                    if check is None:
                        query = queryConstructor(query, columns_info[table_name], list(map(row.get, columns_names[table_name])), ids)
                    else:
                        continue
                else:
                    query_check = 'SELECT Id_, {} FROM {} WHERE {} = \'{}\';'.format\
                        (columns_names[table_name][0], table_name, columns_names[table_name][0], row[columns_names[table_name][0]])
                    check = cursor.execute(query_check).fetchone()

                    if check is None:
                        query = queryConstructor(query, columns_info[table_name], list(map(row.get, columns_names[table_name])))
                    else:
                        ids.append(check[0])
                        continue

                cursor.execute(query)
                ids.append(cursor.execute('SELECT Id_ FROM {} ORDER BY Id_ DESC LIMIT 1;'.format(table_name)).fetchone()[0])