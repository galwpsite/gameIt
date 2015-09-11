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


### All Game Help Functions:
    def getAllGames(self):
        return self.__db_cursor.execute("EXECUTE getAllGames;").fetchall()
    def findGameByName(self,s):
        return self.__db_cursor.execute("""EXECUTE getGameByName ? """,s).fetchall()
    def getNumOfGames(self):
          return len(list(self.getAllGames()))
    def findGameByGameNo(self,s):
        return self.__db_cursor.execute("""EXECUTE getGameByGameNo ? """,s).fetchall()
    def addGame(self,gameNo,gameName,gameDesc):
        print(gameNo,gameName,gameDesc)
        try:
            self.__db_cursor.execute("""addGame  ?,?,? """,gameNo,gameName,gameDesc)
            return True
        except pyodbc.IntegrityError:
            return False


### All Game Help Functions:
    def getNumOfLevels(self):
        return len(list(self.__db_cursor.execute("""EXECUTE getNumOfLevels""").fetchall()))

### All Purchases Help Functions:
    def getNumOfPurchases(self):
        return len(list(self.__db_cursor.execute("""EXECUTE getNumOfPurchases""").fetchall()))

### All User  Help Functions:
    def getAllUsers(self):
        return self.__db_cursor.execute("EXECUTE getAllUsers;").fetchall()
    def getNumOfUsers(self):
      return len(list(self.getAllUsers()))