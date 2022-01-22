from flask import Blueprint, render_template, request
from flask_mysqldb import MySQLdb
from flask.helpers import url_for
from werkzeug.utils import redirect
from app import mysql

colleges = Blueprint('colleges', __name__, url_prefix='/colleges')

# function for colleges homepage
@colleges.route("/")
def collegeshome():
    title = 'Colleges'
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM college ORDER BY college_code")
        data = cursor.fetchall()
        print(data)
        return render_template("colleges.html", college=data, title=title)
    
    except Exception as e:
        return str(e)

# function for add_college page
@colleges.route("/add_collegepage")
def add_collegepage():
    title = 'Add College'
    return render_template("add_college.html", title=title)

# function for edit_college page
@colleges.route("/edit_collegepage/<string:college_code>")
def edit_collegepage(college_code):
    title = 'Edit College'
    # loads data from college table into fields to be edited
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM college WHERE college_code = %s''',(college_code,))
    data = cursor.fetchall()
    cursor.close()
    return render_template("edit_college.html",college_info=data, title=title)

#function for add_college action
@colleges.route("/add_college", methods = ['POST'])
def add_college():
    if request.method == 'POST':
        #requests input from webpage
        college_code = request.form['college_code']
        college_name = request.form['college_name']

        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO college VALUES(%s,%s)''',(college_code, college_name))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("colleges"))

#function for delete_college action
@colleges.route("/delete_college/<string:college_code>", methods = ['GET'])
def delete_college(college_code):
        #removes records from college table through college_code
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM college WHERE college_code = %s''',(college_code,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("colleges"))

#function for edit_college action
@colleges.route("/edit_college/<string:college_code>", methods = ['POST'])
def edit_college(college_code):
    if request.method == 'POST':
        #requests input from webpage
        college_code = request.form['college_code']
        college_name = request.form['college_name']

        #updates records from college table through college_code
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE college SET college_name = %s WHERE college_code = %s''',(college_name, college_code))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("colleges"))
