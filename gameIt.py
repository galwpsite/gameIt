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

Menu(app=app)
flask_breadcrumbs.Breadcrumbs(app=app)


h=helper.Helper()

@app.route('/')
@flask_breadcrumbs.register_breadcrumb(app,'.','Home')
def main():
    #delete later
    return render_template('main.html',numOfGames=h.getNumOfGames(), numOfUsers=h.getNumOfUsers())


@app.route('/home/games',methods=['GET','POST'])
@flask_breadcrumbs.register_breadcrumb(app,'.Games','Games List')
def games():
    if request.method == 'POST':
        form=request.form
        return redirect(url_for("gamesSearch"),code=307)
    posts = [dict(id=row[0],name=row[1],desc=row[2]) for row in h.getAllGames() ]
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
    gameNo = request.args.get('gameNo')
    game= [dict(id=row[0],name=row[1],desc=row[2]) for row in h.findGameByGameNo(gameNo)]
    gameName = (game[0].get('name'))
    gameDesc = (game[0].get('desc'))
    return render_template('edit-game.html',pageTitle="Manage Games",pageSubTitle="Edit Game: "+gameName,gameNo=gameNo,gameName=gameName,gameDesc=gameDesc)



@app.errorhandler(404)
@flask_breadcrumbs.register_breadcrumb(app,'.error','Page Not Found')
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.debug=True
    app.run()
