__author__ = 'galwp'
'''
    This is the "Model" Class, it takes things from our database
'''
import pyodbc
class Helper():
    #Settings:
    connection_str ="""
    Driver={SQL Server Native Client 11.0};
    Server=GAL-PC\SQLEXPRESS;
    Database=gameIt_DBSummer;
    Trusted_Connection=yes;
    """
    __db_connection = pyodbc.connect(connection_str)
    __db_connection.autocommit = True
    __db_cursor = __db_connection.cursor()

    def getAllGames(self):
        return self.__db_cursor.execute("EXECUTE getAllGames;").fetchall()
    def getAllUsers(self):
        return self.__db_cursor.execute("EXECUTE getAllUsers;").fetchall()

    def getNumOfGames(self):
          return len(list(self.getAllGames()))

    def getNumOfUsers(self):
      return len(list(self.getAllUsers()))