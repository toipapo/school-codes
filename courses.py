from flask import Blueprint, render_template, request
from flask_mysqldb import MySQLdb
from flask.helpers import url_for
from werkzeug.utils import redirect
from app import mysql

courses = Blueprint('courses', __name__, url_prefix='/courses')

# function for courses homepage
@courses.route("/")
def courseshome():
    title = 'Courses'
    try:
        #load data from course table into course homepage
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM course ORDER BY college_code")
        data = cursor.fetchall()
        print(data)
        return render_template("courses.html", course=data, title=title)
    
    except Exception as e:
        return str(e)

# function for add_course page
@courses.route("/add_coursepage")
def add_coursepage():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM college''')
    data = cursor.fetchall()
    cursor.close()
    title = 'Add Course'
    return render_template("add_course.html",college_select=data, title=title)

# function for edit_course page
@courses.route("/edit_coursepage/<string:course_code>")
def edit_coursepage(course_code):
    title = 'Edit Course'
    # loads data from course table into fields to be edited
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM course WHERE course_code = %s''',(course_code,))
    data = cursor.fetchall()

    cursor.execute('''SELECT * FROM college''')
    college_data = cursor.fetchall()

    cursor.close()
    return render_template("edit_course.html",course_info=data, college_select=college_data, title=title)

#function for add_course action
@courses.route("/add_course", methods = ['POST'])
def add_course():
    if request.method == 'POST':
        #requests input from webpage
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        college_code = request.form['college_code']

        #plug inputs into database
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO course VALUES(%s,%s,%s)''',(course_code, course_name, college_code))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("courses.courseshome"))

#function for delete_course action
@courses.route("/delete_course/<string:course_code>", methods = ['GET'])
def delete_course(course_code):
        #removes records from course table through course_code
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM course WHERE course_code = %s''',(course_code,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("courses.courseshome"))

#function for edit_course action
@courses.route("/edit_course/<string:course_code>", methods = ['POST'])
def edit_course(course_code):
    if request.method == 'POST':
        #requests input from webpage
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        college_code = request.form['college_code']

        #updates records from course table through course_code
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE course SET course_name = %s, college_code = %s WHERE course_code = %s''',(course_name, college_code, course_code))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("courses.courseshome"))