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

app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = '3nMN*sBNjh#pjG*yGSKBZ5&ePG2eAmc^pcGG7KYXtSugvb2Ee$rW9$6gSNRpeAU$%BrfpGkhvHV6@heD2RTQ2pbk9cwHwAZVMyKz'

Menu(app=app)
flask_breadcrumbs.Breadcrumbs(app=app)


h=helper.Helper()

@app.route('/')
@flask_breadcrumbs.register_breadcrumb(app,'.','Home')
def main():
    #delete later
    return render_template('main.html',numOfGames=h.getNumOfGames(), numOfUsers=h.getNumOfUsers(),numOfLevels=h.getNumOfLevels(),numOfPurchases=h.getNumOfPurchases())


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
    gameName = (game[0].get('name'))
    gameDesc = (game[0].get('desc'))
    return render_template('edit-game.html',pageTitle="Manage Games",pageSubTitle="Edit Game: "+gameName,gameNo=gameNo,gameName=gameName,gameDesc=gameDesc,
                           gameCriteria=gameCriteria,gameUnusedCriteria=gameUnusedCriteria,showCriteria=True)

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

@app.errorhandler(404)
@flask_breadcrumbs.register_breadcrumb(app,'.error','Page Not Found')
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.debug=True
    app.run()
