__author__ = 'galwp'
'''
    This is the "Model" Class, it takes things from our database
'''
import pyodbc
class Helper():
    #Settings:
    connection_str ="""
    Driver={SQL Server Native Client 10.0};
    Server=DESKTOP-SL551FH\SQLEXPRESS;
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
        try:
            self.__db_cursor.execute("""EXECUTE addGame  ?,?,? """,gameNo,gameName,gameDesc)
            return True
        except pyodbc.IntegrityError:
            return False

    def getCriteriaByCode(self,s):
        return self.__db_cursor.execute("""EXECUTE getCriteriaByCode ? """,s).fetchall()

    def updateGame (self,gameNo,gameName,gameDesc):
        try:
            self.__db_cursor.execute("""EXECUTE updateGame  ?,?,? """,gameNo,gameName,gameDesc)
            return True
        except pyodbc.IntegrityError:
            return False

    def getGameCriteria (self,gameNo):
        return self.__db_cursor.execute("""EXECUTE getGameCriteria ? """,gameNo).fetchall()

    def getGameUnusedCriteria (self,gameNo):
        return self.__db_cursor.execute("""EXECUTE getGameUnusedCriteria ? """,gameNo).fetchall()

    def addCriteriaToGame (self,cCode,gameNo):
            self.__db_cursor.execute("""EXECUTE addCriteriaToGame  ?,? """,cCode,gameNo)

    def removeCriteriaFromGame (self,cCode):
            self.__db_cursor.execute("""EXECUTE removeCriteriaFromGame  ? """,cCode)

    def getFreeGameCriteria(self):
        return self.__db_cursor.execute("""EXECUTE getFreeGameCriteria """).fetchall()



    def addCrit(self,critNo,critName,critAmount):
        try:
            self.__db_cursor.execute("""EXECUTE addCrit  ?,?,? """,critNo,critName,critAmount)
            return True
        except pyodbc.IntegrityError:
            return False

    def findCritByCode(self,s):
        return self.__db_cursor.execute("""EXECUTE findCrit ? """,s).fetchall()

    def findGameCritByCode(self,s):
        return self.__db_cursor.execute("""EXECUTE findGameCritByCode ? """,s).fetchall()

    def getGameCritGame(self,s):
        return self.__db_cursor.execute("""EXECUTE getGameCritGame ? """,s).fetchall()

    def removeGameCriteria(self,critNo):
        try:
            self.__db_cursor.execute("""EXECUTE removeGameCriteria  ?""",critNo)
            return True
        except pyodbc.IntegrityError:
            return False

    def makeGameCriteria(self,critNo):
        try:
            self.__db_cursor.execute("""EXECUTE makeGameCriteria  ?""",critNo)
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


    def getAllCriterias(self):
        return self.__db_cursor.execute("""EXECUTE getAllCriterias """).fetchall()

    def reportLevelInfo(self):
        return self.__db_cursor.execute("""EXECUTE reportLevelInfo """).fetchall()

    def reportPurchasePerYear(self):
        return self.__db_cursor.execute("""EXECUTE reportPurchasePerYear """).fetchall()

    def reportUsersWithXFriends(self,x):
        return self.__db_cursor.execute("""EXECUTE reportUsersWithXFriends ?""",x).fetchall()

    def reportMostBoringLevelOfAGame(self,x):
        return self.__db_cursor.execute("""EXECUTE reportMostBoringLevelOfAGame ?""",x).fetchall()


    def getUserWithMostPointInGameX(self,x):
        return self.__db_cursor.execute("""EXECUTE getUserWithMostPointInGameX ?""",x).fetchall()

    def reportGetUsersWhoPlayedYLevelInGameX(self,x,y):
        return self.__db_cursor.execute("""EXECUTE getUserWithMostPointInGameX ?, ?""",x,y).fetchall()


    def getNumOfDownloadInGameXatMonthY(self,x,y):
        return self.__db_cursor.execute("""EXECUTE getNumOfDownloadInGameXatMonthY ?,?""",x,y).fetchall()

    def getUsersWhoDownloadedGameX(self,x):
        return self.__db_cursor.execute("""EXECUTE getUsersWhoDownloadedGameX ?""",x).fetchall()

    def getUserByID(self,x):
        return self.__db_cursor.execute("""EXECUTE getUserByID ?""",x).fetchall()

    def getGamesWhichWereDownloadedByUserX(self,x):
        return self.__db_cursor.execute("""EXECUTE getGamesWhichWereDownloadedByUserX ?""",x).fetchall()


    def getFriendsOfUserX(self,x):
        return self.__db_cursor.execute("""EXECUTE getFriendsOfUserX ?""",x).fetchall()

