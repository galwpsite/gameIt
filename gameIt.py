'''
    This is the Controller Class
'''
from flask import Flask,render_template, request, session, flash, redirect, url_for, g
from functools import wraps
from flask import g, request, redirect, url_for
import pyodbc
import helper
import flask_breadcrumbs
from flask_menu import Menu, register_menu
import csv
from io import TextIOWrapper


app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = '3nMN*sBNjh#pjG*yGSKBZ5&ePG2eAmc^pcGG7KYXtSugvb2Ee$rW9$6gSNRpeAU$%BrfpGkhvHV6@heD2RTQ2pbk9cwHwAZVMyKz'
UPLOAD_FOLDER = 'c:/gameIt/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Menu(app=app)
flask_breadcrumbs.Breadcrumbs(app=app)


h=helper.Helper()

@app.route('/')
@flask_breadcrumbs.register_breadcrumb(app,'.','Home')
def main():
    return render_template('main.html',numOfGames=h.getNumOfGames(), numOfUsers=h.getNumOfUsers(),numOfLevels=h.getNumOfLevels(),numOfPurchases=h.getNumOfPurchases())


@app.route('/home/reports')
@flask_breadcrumbs.register_breadcrumb(app,'.Reports','Manage Reports')
def mainReports():
    games= [dict(id=row[0],name=row[1],desc=row[2],c="") for row in h.getAllGames() ]
    return render_template('reports-main.html',games=games)


@app.route('/home/reports/show',methods=['GET'])
@flask_breadcrumbs.register_breadcrumb(app,'.Reports','Manage Reports')
def showReport():
    q=request.args.get('q')
    if q=='1':
        rows = [dict(r1=row[0],r2=row[1],r3=row[2],r4=row[3],r5=row[4],r6=row[5]
                      ,r7=row[6],r8=row[7]) for row in h.reportLevelInfo() ]
        return render_template('report-q1.html',title="Level Information",rows=rows)

    elif (q=='2'):
            rows = [dict(r1=row[0],r2=row[1],r3=row[1],r4=row[3],r5=row[4],r6=row[5],r7=row[6]
                      ,r8=row[7]) for row in h.reportPurchasePerYear() ]
            return render_template('report-q2.html',title="Level Information",rows=rows)

    elif (q=='3'):
            xval=request.args.get('x')
            rows = [dict(r1=row[0],r2=row[1],r3=row[1],r4=row[3],r5=row[4],r6=row[5]) for row in h.reportUsersWithXFriends(xval) ]
            return render_template('report-q3.html',title="Friends with "+xval+" Game Requests which where sent by "+str(0.3*float(xval))+" diffrent friends",rows=rows)
    elif (q=='4'):
            xval=request.args.get('x')
            rows = [dict(r1=row[0],r2=row[1],r3=row[1],r4=row[3],r5=row[4],r6=row[5]) for row in h.reportMostBoringLevelOfAGame(xval) ]
            return render_template('report-q4.html',title="The most boring level in a specif game" ,rows=rows)
    elif (q=='5'):
            xval=request.args.get('x')
            rows = [dict(r1=row[0],r2=row[1],r3=row[1]) for row in h.getUserWithMostPointInGameX(xval) ]
            game=[dict(r1=row[0],r2=row[1]) for row in h.findGameByGameNo(xval)]
            return render_template('report-q5.html',title="The users who are best among their friends in " + game[0].get('r2') ,rows=rows)
    elif (q=='6'):
            xval=request.args.get('x')
            yval=request.args.get('y')
            rows = [dict(r1=row[0],r2=row[1],r3=row[1]) for row in h.getUserWithMostPointInGameX(xval) ]
            game=[dict(r1=row[0],r2=row[1]) for row in h.findGameByGameNo(xval)]
            return render_template('report-q5.html',title="The users who are best among their friends in " + game[0].get('r2') ,rows=rows)
    return render_template('reports-main.html')

@app.route('/home/games',methods=['GET','POST'])
@flask_breadcrumbs.register_breadcrumb(app,'.Games','Games List')
def games():
    if request.method == 'POST':
        form=request.form
        return redirect(url_for("gamesSearch"),code=307)
    posts = [dict(id=row[0],name=row[1],desc=row[2],c="") for row in h.getAllGames() ]
    for p in posts:
        p['c']=[dict(cNo=row[0],cName=row[1])  for row in h.getGameCriteria(p['id'])]
    return render_template('archive-game.html',pageTitle="Manage Games",pageSubTitle="List Of All The Games: ",posts=posts)

@app.route('/home/games/search',methods=['GET','POST'])
@flask_breadcrumbs.register_breadcrumb(app,'.Games.Search','Search Results')
def gamesSearch():
    form=request.form
    posts = [dict(id=row[0],name=row[1],desc=row[2]) for row in h.findGameByName(form['name']) ]
    return render_template('archive-game.html',pageTitle="Manage Games",pageSubTitle="List Of All The Games: ",posts=posts)

@app.route('/home/games/edit',methods=['GET','POST'])
@flask_breadcrumbs.register_breadcrumb(app,'.Games.Edit','Edit Game')
def gameEdit():
    if request.method == 'POST':
            form=request.form
            if 'search-form' in form:
                return redirect(url_for("gamesSearch"),code=307)
            else: #If it was the edit form:
                form=request.form
                gameNo=(form['id'])
                gameName = (form['name'])
                gameDesc = (form['desc'])
                if h.updateGame(int(gameNo),gameName,gameDesc):
                    flash("The game "+gameName+" successfully updated.")
                else :
                    flash("Something went wrong",'error')
    gameNo = request.args.get('gameNo')
    game= [dict(id=row[0],name=row[1],desc=row[2]) for row in h.findGameByGameNo(gameNo)]
    gameCriteria=[dict(cNo=row[0],cName=row[1])  for row in h.getGameCriteria(gameNo)]
    gameUnusedCriteria = [dict(cNo=row[0],cName=row[1])  for row in h.getFreeGameCriteria()]
    users = [dict(r1=row[0],r2=row[1])  for row in h.getUsersWhoDownloadedGameX(gameNo)]
    gameName = (game[0].get('name'))
    gameDesc = (game[0].get('desc'))
    gameDownloads=[]
    for month in range (1,13):
        try:
            gameDownloads.append([dict(r1=row[0])  for row in h.getNumOfDownloadInGameXatMonthY(gameNo,month)][0].get('r1'))
        except IndexError:
            gameDownloads.append(0)
        print ("month "+ str(month) +" downloads: " + str(gameDownloads[month-1]))
    return render_template('edit-game.html',pageTitle="Manage Games",pageSubTitle="Edit Game: "+gameName,gameNo=gameNo,gameName=gameName,gameDesc=gameDesc,
                           gameCriteria=gameCriteria,gameUnusedCriteria=gameUnusedCriteria,showCriteria=True,gameDownloads=gameDownloads,users=users)

@app.route('/home/games/add',methods=['GET','POST'])
@flask_breadcrumbs.register_breadcrumb(app,'.Games.Add','Add Game')
def gameAdd():
    if request.method == 'POST':
            form=request.form
            if 'search-form' in form:
                return redirect(url_for("gamesSearch"),code=307)
            else: #If it was the edit form:
                form=request.form
                gameNo=(form['id'])
                gameName = (form['name'])
                gameDesc = (form['desc'])
                if h.addGame(int(gameNo),gameName,gameDesc):
                    flash("The game "+gameName+" successfully added")
                    return  render_template('edit-game.html',pageTitle="Manage Games",pageSubTitle="Add New Game:",gameNo=gameNo,gameName=gameName,gameDesc=gameDesc)
                else :
                    flash("Something went wrong (maybe GameNo already exist?)",'error')
    return  render_template('edit-game.html',pageTitle="Manage Games",pageSubTitle="Add New Game:",gameNo="",gameName="",gameDesc="")

@app.route('/addCriteriaToGame',methods=['GET','POST'])
def addCriteriaToGame():
    gameNo = request.args.get('gameNo')
    cCode = request.args.get('cCode')
    h.addCriteriaToGame(cCode,gameNo)
    return "<script>window.close();</script>"

@app.route('/removeCriteriaFromGame',methods=['GET','POST'])
def removeCriteriaFromGame():
    cCode = request.args.get('cCode')
    h.removeCriteriaFromGame(cCode)
    return "<script>window.close();</script>"

@app.route('/makeGameCriteria',methods=['GET','POST'])
def makeGameCriteria():
    cCode = request.args.get('cCode')
    h.makeGameCriteria(cCode)
    return "<script>window.close();</script>"


@app.route('/home/criteria',methods=['GET','POST'])
@flask_breadcrumbs.register_breadcrumb(app,'.Criterias','Criterias List')
def criterias():
    if request.method == 'POST':
        form=request.form
        return redirect(url_for("gamesSearch"),code=307)
    allCriterias = [dict(id=row[0],name=row[1],amount=row[2],gameName=row[3],gameNo=row[4]) for row in h.getAllCriterias() ]
    for c in allCriterias:
        try:
            h.findGameCritByCode(c.get('id'))[0]
            c['type']='gameCriteria'
        except IndexError:
            c['type']='normalCriteria'

    return render_template('archive-criterias.html',pageTitle="Manage Criterias",pageSubTitle="List Of All The Criterias: ",allCriterias=allCriterias)


@app.route('/home/criteria/add',methods=['GET','POST'])
@flask_breadcrumbs.register_breadcrumb(app,'.Criterias.Add','Add Criteria')
def criteriaAdd():
    if request.method == 'POST':
            form=request.form
            if 'search-form' in form:
                return redirect(url_for("gamesSearch"),code=307)
            else: #If it was the edit form:
                form=request.form
                critNo=(form['id'])
                critName = (form['critName'])
                critAmount = (form['critAmount'])
                if h.addCrit(critNo,critName,critAmount):
                    flash("The Criteria "+critName+" successfully added")
                    return  render_template('edit-criteria.html',pageTitle="Manage Games",pageSubTitle="Add New Game:",critNo=critNo,critName=critName,critAmount=critAmount)
                else :
                    flash("Something went wrong (maybe GameNo already exist?)",'error')
    return  render_template('edit-criteria.html',pageTitle="Manage Criteria",pageSubTitle="Add New Criteria:",critNo="",critName="",critAmount="")

@app.route('/home/criteria/edit',methods=['GET','POST'])
@flask_breadcrumbs.register_breadcrumb(app,'.Criterias.Edit','Edit Criteria')
def criteriaEdit():
    if request.method == 'POST':
            form=request.form
            if 'search-form' in form:
                return redirect(url_for("gamesSearch"),code=307)
            else: #If it was the edit form:
                form=request.form
                critNo=(form['id'])
                critName = (form['critName'])
                critAmount = (form['critAmount'])
                if h.updateGame(int(critNo),critName,critAmount):
                    flash("The game "+critName+" successfully updated.")
                else :
                    flash("Something went wrong",'error')
    critNo = request.args.get('cCode')
    crit= [dict(id=row[0],name=row[1],amount=row[2]) for row in h.findCritByCode(critNo)]
    critName = (crit[0].get('name'))
    critAmount = (crit[0].get('amount'))
    game=None
    isGameCrit = True
    attached=False
    if not h.findGameCritByCode(critNo):
       isGameCrit=False;
    if isGameCrit:
        attached=True
        #Get the attached game
        game=[dict(id=row[0],name=row[1]) for row in h.getGameCritGame(critNo)]
        if not game:
            attached=False
    return render_template('edit-criteria.html',pageTitle="Manage Criteria",pageSubTitle="Edit Criteria: "+critName,critNo=critNo,critName=critName,critAmount=critAmount,
                           isGameCrit=isGameCrit,game=game,attached=attached)

@app.route('/removeGameCriteria',methods=['GET','POST'])
def removeGameCriteria():
    cCode = request.args.get('cCode')
    print (cCode)
    h.removeGameCriteria(cCode)
    return "<script>window.close();</script>"


@app.route('/userView',methods=['GET','POST'])
@flask_breadcrumbs.register_breadcrumb(app,'.User','User')
def userView():
    id = request.args.get('id')
    user=[dict(r1=row[0],r2=row[1],r3=row[2],r4=row[3]) for row in h.getUserByID(id)]
    games = [dict(r1=row[0],r2=row[1]) for row in h.getGamesWhichWereDownloadedByUserX(id)]
    friendsID = [dict(r1=row[4],r2=row[5]) for row in h.getFriendsOfUserX(id)]
    friends=[]
    for friendID in friendsID:
        if int(friendID.get('r2')) == int(id):
            print ("boom")
            friends.append([dict(r1=row[0],r2=row[1],r3=row[2],r4=row[3]) for row in h.getUserByID(friendID.get('r1'))][0])
        else:
            friends.append([dict(r1=row[0],r2=row[1],r3=row[2],r4=row[3]) for row in h.getUserByID(friendID.get('r2'))][0])
    return render_template('view-user.html',user=user[0],games=games,friends=friends)

@app.route('/importFile',methods=['GET','POST'])
@flask_breadcrumbs.register_breadcrumb(app,'.Import','Import')
def importFile():
    if request.method == 'POST':
        form=request.form
        file = request.files['file']
        dataType=form['dataType']
        file.save('c:/uploads/temp.csv')
        data=[]
        with open('c:/uploads/temp.csv', 'rb') as csvfile:
            spamreader = csv.reader(TextIOWrapper(csvfile),dialect='excel', quotechar='|')
            for entity in spamreader:
                i=0
                if dataType=='tblUser':
                    for row in entity:
                        data.append(row)
                        print (row)
                        i+=1
                        if i>=4:
                            if (h.adduser(data[0],data[1],data[2],data[3])):
                                flash("User  " + data[2]+" was successfully added")
                            else:
                                flash("Could not add the user " + data[2]+" Maybe ID("+data[0]+") already exit?",'error')
                            data=[]
                            break
    return render_template('import.html')

@app.errorhandler(404)
@flask_breadcrumbs.register_breadcrumb(app,'.error','Page Not Found')
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.debug=True
    app.run()
