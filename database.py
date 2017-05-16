import os
import sys
import sqlite3


class Database:
    __shared_state = None

    def __init__(self, database_name, sql_script_name, database_path=None):
        if self.__shared_state is None:
            if database_path is not None and os.path.exists(database_path):
                os.chdir(database_path)

            try:
                self.db = sqlite3.connect(database_name)

            except sqlite3.Error as e:
                print("Error: %s :" % e.args[0])
                sys.exit()

            else:
                self.init_database(sql_script_name)
                self.db.row_factory = sqlite3.Row
                self.c = self.db.cursor()

            self.__shared_state = self.__dict__
        else:
            self.__dict__ = self.__shared_state

    def init_database(self, script_name):
        try:
            file = open(script_name, 'r')

        except IOError:
            print("Error: SQL file does not exist")
            sys.exit()

        else:
            script = file.read()

        finally:
            if file is not None:
                file.close()

        try:
            self.db.executescript(script)

        except sqlite3.OperationalError:
            print("The tables already exist")

        else:
            self.db.commit()

    # useful or not?
    def write_entry(self, table, entry):

        columns = ', '.join(entry.keys())
        placeholders = ':'+', :'.join(entry.keys())

        sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table, columns, placeholders)

        try:
            self.c.execute(sql, entry)

        except sqlite3.Error as e:
            print("Error: %s :" % e.args[0])

        else:
            self.db.commit()

    #TODO: put the table name in the entries_list (entries in different table)
    def write_entries(self, table, entries_list):

        for entry in entries_list:

            columns = ', '.join(entry.keys())
            placeholders = ':' + ', :'.join(entry.keys())

            sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table, columns, placeholders)

            try:
                self.c.execute(sql, entry)

            except sqlite3.Error as e:
                print("Error: %s :" % e.args[0])

            else:
                self.db.commit()

    def read_entry(self, table, columns, conditions):

        tab = []
        data = None
        data_dict = {}

        columns = ', '.join(columns)

        for key, value in conditions.items():
            if type(value) is str:
                tab.append('%s = "%s"' % (key, value))
            else:
                tab.append('%s = %s' % (key, str(value)))

        conditions = ' AND '.join(tab)

        sql = 'SELECT %s FROM %s WHERE %s' % (columns, table, conditions)

        try:
            self.c.execute(sql)

        except sqlite3.Error as e:
            print("Error: %s :" % e.args[0])

        else:
            data = self.c.fetchone()

            for key in data.keys():
                data_dict[key] = data[key]

        return data_dict

    def read_entries(self, table, columns, conditions=None, limit=None, offset=None):
        data = None
        data_list = []
        sql = ''
        columns_size = len(columns)
        columns = ', '.join(columns)

        if conditions is not None:
            tab = []

            for key, value in conditions.items():
                if type(value) is str:
                    tab.append('%s = "%s"' % (key, value))
                else:
                    tab.append('%s = %s' % (key, str(value)))

            conditions = ' AND '.join(tab)

            sql = 'SELECT %s FROM %s WHERE %s' % (columns, table, conditions)
        else:
            sql = 'SELECT %s FROM %s' % (columns, table)

        if limit is not None:
            sql += ' LIMIT %s' % (str(limit))
        if offset is not None:
            sql += ' OFFSET %s' % (str(offset))

        try:
            self.c.execute(sql)

        except sqlite3.Error as e:
            print("Error: %s :" % e.args[0])

        else:
            for data in self.c.fetchall():
                if columns_size == 1:
                    for key in data.keys():
                        data_list.append(data[key])
                else:
                    data_list.append({})

                    for key in data.keys():
                        data_list[len(data_list)-1][key] = data[key]

        return data_list

    def increment_entry(self, table, column, conditions):
        tab = []

        for key, value in conditions.items():
            if type(value) is str:
                tab.append('%s = "%s"' % (key, value))
            else:
                tab.append('%s = %s' % (key, str(value)))

        conditions = ' AND '.join(tab)

        sql = 'UPDATE %s SET %s = %s + 1 WHERE %s' % (table, column, column, conditions)

        try:
            query = self.c.execute(sql)

        except sqlite3.Error as e:
            print("Error: %s :" % e.args[0])

        else:
            self.db.commit()