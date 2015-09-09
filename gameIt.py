from flask import Flask,render_template, request, session, flash, redirect, url_for, g
from functools import wraps
from flask import g, request, redirect, url_for
import pyodbc
import helper
app = Flask(__name__)
h=helper.Helper()
@app.route('/')
def main():
    #delete later
    return render_template('main.html',numOfGames=h.getNumOfGames(), numOfUsers=h.getNumOfUsers())




if __name__ == '__main__':
    app.debug=True
    app.run()
